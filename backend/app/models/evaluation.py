import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base  # Adjust import based on your project structure


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_version = Column(String, nullable=False)
    run_type = Column(String, nullable=False)  # retrieval, generation, safety, full
    status = Column(
        String, nullable=False, default="pending"
    )  # pending, running, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    configuration = Column(JSON, nullable=True)
    summary = Column(JSON, nullable=True)
    report_path = Column(String, nullable=True)
    created_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    results = relationship(
        "EvaluationResult", back_populates="run", cascade="all, delete-orphan"
    )


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, ForeignKey("evaluation_runs.id"), nullable=False)
    query_id = Column(String, nullable=False)
    category = Column(String, nullable=True)
    difficulty = Column(String, nullable=True)

    # Metrics stored as JSON for flexibility
    retrieval_metrics = Column(JSON, nullable=True)
    generation_metrics = Column(JSON, nullable=True)
    safety_outcomes = Column(JSON, nullable=True)

    failure_category = Column(String, nullable=True)
    details = Column(JSON, nullable=True)

    run = relationship("EvaluationRun", back_populates="results")
