from app.database import get_db
from app.jobs.document_tasks import process_document_task
from app.models.background_job import JobType
from app.services.background_job_service import BackgroundJobService
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


class DocumentUploadResponse(BaseModel):
    job_id: str
    status: str
    message: str


@router.post(
    "/upload",
    response_status=status.HTTP_202_ACCEPTED,
    response_model=DocumentUploadResponse,
)
def upload_and_process_document(file_id: str, db: Session = Depends(get_db)):
    # 1. Initialize job service
    job_service = BackgroundJobService(db)

    # 2. Create durable job record in PostgreSQL
    # Replace "current-user-id" with your actual authenticated user dependency
    job = job_service.create_job(
        job_type=JobType.DOCUMENT_PROCESSING,
        created_by="current-user-id",
        resource_id=file_id,
    )

    # 3. Trigger the Celery task asynchronously using .delay()
    # Pass IDs, never full file contents or database objects
    task = process_document_task.delay(document_id=file_id, job_id=job.id)

    # 4. Save the Celery task_id to the job record for tracking
    job_service.repo.update_status(job.id, job.status, task_id=task.id)

    return {
        "job_id": job.id,
        "status": "pending",
        "message": "Document upload accepted and queued for processing.",
    }
