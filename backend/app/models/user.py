import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    String,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.mixins import TimestampMixin


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    STUDENT = "student"
    GUEST = "guest"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(
            UserRole,
            name="user_role",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=UserRole.STUDENT,
        server_default="student",
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="1",
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="0",
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(
            UserRole,
            name="user_role",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=UserRole.STUDENT,
        server_default="student",
        nullable=False,
    )
