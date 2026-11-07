import json
import logging

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.services.conversation_service import ConversationService
from app.services.rag_service import RagService
from app.services.streaming_chat_service import StreamingChatService
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

logger = logging.getLogger("medical-rag")

router = APIRouter()

rag_service = RagService()
streaming_chat_service = StreamingChatService()
conversation_service = ConversationService()


class ChatRequest(BaseModel):
    question: str
    conversation_id: int | None = None


def sse_event(event_type: str, data: dict) -> str:
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


# ---------------------------------------------------------
# NORMAL CHAT ENDPOINT
# ---------------------------------------------------------


@router.post("/")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # Create a new conversation or load an existing one.
        if request.conversation_id is None:
            conversation = conversation_service.create_conversation(
                db=db,
                user_id=current_user.id,
                title=request.question[:255],
            )
            conversation_history = []
        else:
            conversation = conversation_service.get_conversation(
                db=db,
                conversation_id=request.conversation_id,
                user_id=current_user.id,
            )

            if conversation is None:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found",
                )

            conversation_history = conversation_service.get_messages(
                db=db,
                conversation_id=request.conversation_id,
                user_id=current_user.id,
            )

        # Save the user's message.
        saved_message = conversation_service.add_message(
            db=db,
            conversation_id=conversation.id,
            user_id=current_user.id,
            role="user",
            content=request.question,
        )

        if saved_message is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        # Generate the RAG answer and log any error.
        try:
            result = await rag_service.answer(
                request.question,
                conversation_history=conversation_history,
            )
        except Exception:
            logger.exception("Chat request failed while generating RAG answer")
            raise

        # Save the assistant's answer.
        saved_message = conversation_service.add_message(
            db=db,
            conversation_id=conversation.id,
            user_id=current_user.id,
            role="assistant",
            content=result["answer"],
        )

        if saved_message is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        return {
            "answer": result["answer"],
            "related_topics": result.get("related_topics", []),
            "conversation_id": conversation.id,
        }

    except HTTPException:
        raise
    except Exception:
        logger.exception("Normal chat endpoint failed")
        raise


# ---------------------------------------------------------
# STREAMING CHAT ENDPOINT
# ---------------------------------------------------------


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    http_request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if request.conversation_id is None:
        conversation = conversation_service.create_conversation(
            db=db,
            user_id=current_user.id,
            title=request.question[:255],
        )
        conversation_history = []
    else:
        conversation = conversation_service.get_conversation(
            db=db,
            conversation_id=request.conversation_id,
            user_id=current_user.id,
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        conversation_history = conversation_service.get_messages(
            db=db,
            conversation_id=request.conversation_id,
            user_id=current_user.id,
        )

    conversation_id = conversation.id

    saved_user_message = conversation_service.add_message(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        role="user",
        content=request.question,
    )

    if saved_user_message is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    async def event_generator():
        yield sse_event(
            "START",
            {"conversation_id": conversation_id},
        )

        full_answer = ""

        try:
            async for event in streaming_chat_service.stream_answer(
                request.question,
                conversation_history=conversation_history,
            ):
                if await http_request.is_disconnected():
                    logger.info("Streaming client disconnected")
                    return

                if event.type == "token":
                    full_answer += event.content
                    yield sse_event(
                        "TOKEN",
                        {"content": event.content},
                    )

                elif event.type == "error":
                    logger.error("Streaming chat error: %s", event.content)
                    yield sse_event(
                        "ERROR",
                        {"message": event.content},
                    )
                    return

                elif event.type == "done":
                    saved_assistant_message = conversation_service.add_message(
                        db=db,
                        conversation_id=conversation_id,
                        user_id=current_user.id,
                        role="assistant",
                        content=full_answer,
                    )

                    if saved_assistant_message is None:
                        yield sse_event(
                            "ERROR",
                            {"message": "Failed to save assistant response"},
                        )
                        return

                    yield sse_event(
                        "CITATIONS",
                        {"citations": []},
                    )
                    yield sse_event(
                        "COMPLETE",
                        {"conversation_id": conversation_id},
                    )

        except Exception as exc:
            logger.exception("Streaming chat endpoint failed")
            yield sse_event(
                "ERROR",
                {"message": str(exc)},
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


# ---------------------------------------------------------
# GET CONVERSATION MESSAGES
# ---------------------------------------------------------


@router.get("/{conversation_id}/messages")
def get_messages(
    conversation_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    messages = conversation_service.get_messages(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
        limit=limit,
        offset=offset,
    )

    return [
        {
            "id": message.id,
            "conversation_id": message.conversation_id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
        }
        for message in messages
    ]


# ---------------------------------------------------------
# DELETE CONVERSATION
# ---------------------------------------------------------


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = conversation_service.delete_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "message": "Conversation deleted successfully",
        "conversation_id": conversation_id,
    }
