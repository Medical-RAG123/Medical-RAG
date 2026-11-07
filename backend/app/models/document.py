from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.mixins import TimestampMixin


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"
    DELETED = "deleted"


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
    )

    file_extension: Mapped[str] = mapped_column(
        String(20),
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    upload_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    status: Mapped[DocumentStatus] = mapped_column(
        default=DocumentStatus.UPLOADED,
    )

    checksum: Mapped[str] = mapped_column(
        String(128),
    )
