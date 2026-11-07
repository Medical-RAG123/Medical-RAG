import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy import Enum as SQLEnum

from app.database import Base


class JobType(str, enum.Enum):
    DOCUMENT_PROCESSING = "document_processing"
    REINDEX = "reindex"
    EVALUATION = "evaluation"


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    RETRY = "retry"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BackgroundJob(Base):
    __tablename__ = "background_jobs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True, nullable=True)
    job_type = Column(SQLEnum(JobType), nullable=False)
    status = Column(
        SQLEnum(JobStatus), default=JobStatus.PENDING, nullable=False, index=True
    )
    created_by = Column(String, nullable=False, index=True)
    resource_id = Column(String, nullable=True, index=True)
    progress = Column(Float, default=0.0)
    attempt_count = Column(Integer, default=0, nullable=False)
    error_code = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
