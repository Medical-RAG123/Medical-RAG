# your existing imports...

router = APIRouter()

rag_service = RagService()
conversation_service = ConversationService()


@router.post("", response_model=ChatResponse)
async def chat(
    question: str,
    conversation_id: int | None = None,
    db: Session = Depends(get_db),
):
    # your existing chat code...
    ...


@router.get("/{conversation_id}/messages")
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = conversation_service.get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=1,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

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
