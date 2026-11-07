import structlog
from app.database import SessionLocal
from app.jobs.celery_app import celery_app
from app.models.background_job import JobStatus
from app.repositories.background_job_repository import BackgroundJobRepository

logger = structlog.get_logger()


@celery_app.task(
    bind=True,
    name="medical_rag.process_document",
    max_retries=3,
)
def process_document_task(self, document_id: str, job_id: str):
    db = SessionLocal()
    repo = BackgroundJobRepository(db)
    try:
        repo.update_status(
            job_id, JobStatus.RUNNING, attempt_count=self.request.retries + 1
        )
        logger.info(
            "processing_document_started", document_id=document_id, job_id=job_id
        )

        # TODO: Integrate your existing document pipeline services here

        repo.update_status(job_id, JobStatus.COMPLETED, progress=100.0)
        logger.info(
            "processing_document_completed", document_id=document_id, job_id=job_id
        )
    except Exception as exc:
        logger.error(
            "processing_document_failed",
            document_id=document_id,
            job_id=job_id,
            error=str(exc),
        )
        repo.update_status(
            job_id,
            JobStatus.RETRY
            if self.request.retries < self.max_retries
            else JobStatus.FAILED,
            error_code="PROCESSING_ERROR",
            error_message=str(exc),
        )
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()
