from app.models.conversation import Conversation
from app.models.message import Message
from sqlalchemy import select
from sqlalchemy.orm import Session


class ConversationService:
    def create_conversation(
        self,
        db: Session,
        user_id: int,
        title: str | None = None,
    ) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def get_conversation(
        self,
        db: Session,
        conversation_id: int,
        user_id: int,
    ) -> Conversation | None:
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )

        return db.scalar(statement)

    def get_messages(
        self,
        db: Session,
        conversation_id: int,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Message]:
        statement = (
            select(Message)
            .join(
                Conversation,
                Message.conversation_id == Conversation.id,
            )
            .where(
                Message.conversation_id == conversation_id,
                Conversation.user_id == user_id,
            )
            .order_by(
                Message.created_at.asc(),
                Message.id.asc(),
            )
            .limit(limit)
            .offset(offset)
        )

        return list(db.scalars(statement).all())

    def add_message(
        self,
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def delete_conversation(
        self,
        db: Session,
        conversation_id: int,
        user_id: int,
    ) -> bool:
        conversation = self.get_conversation(
            db=db,
            conversation_id=conversation_id,
            user_id=user_id,
        )

        if conversation is None:
            return False

        db.delete(conversation)
        db.commit()

        return True
