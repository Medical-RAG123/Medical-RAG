from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:
    def get_by_conversation(
        self,
        db: Session,
        conversation_id: int,
    ) -> list[Message]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(
                Message.created_at.asc(),
                Message.id.asc(),
            )
        )

        return list(db.scalars(statement).all())

    def create(
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
