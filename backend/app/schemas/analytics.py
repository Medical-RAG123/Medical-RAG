from datetime import datetime

from pydantic import BaseModel


class DocumentSummary(BaseModel):
    total: int
    indexed: int
    processing: int
    failed: int
    total_chunks: int
    total_vectors: int


class EvaluationSummary(BaseModel):
    latest_run_id: str | None
    dataset_version: str | None
    status: str | None
    completed_at: datetime | None
    recall_at_5: float | None
    groundedness: float | None
    citation_coverage: float | None


class AdminOverviewResponse(BaseModel):
    generated_at: datetime
    documents: DocumentSummary
    retrieval: EvaluationSummary
    generation: EvaluationSummary


class HealthComponentStatus(BaseModel):
    database: str
    vector_store: str
    document_storage: str
    llm_provider: str


class SystemHealthResponse(BaseModel):
    status: str
    checked_at: datetime
    components: HealthComponentStatus
