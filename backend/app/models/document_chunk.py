from app.database import SessionLocal
from app.jobs.celery_app import celery_app
from app.models.background_job import JobStatus
from app.repositories.background_job_repository import BackgroundJobRepository


@celery_app.task(
    bind=True,
    name="medical_rag.process_document",
    max_retries=3,
    default_retry_delay=10,
)
def process_document_task(self, document_id: str, job_id: str):
    db = SessionLocal()
    repo = BackgroundJobRepository(db)
    try:
        repo.update_status(job_id, JobStatus.RUNNING, task_id=self.request.id)

        # Call existing processing/indexing pipeline here

        repo.update_status(job_id, JobStatus.COMPLETED, progress=1.0)
    except Exception as exc:
        attempt = self.request.retries + 1
        if attempt < self.max_retries:
            repo.update_status(
                job_id, JobStatus.RETRY, attempt_count=attempt, error_message=str(exc)
            )
            raise self.retry(exc=exc)
        else:
            repo.update_status(
                job_id,
                JobStatus.FAILED,
                attempt_count=attempt,
                error_code="PROCESSING_ERROR",
                error_message=str(exc),
            )
    finally:
        db.close()


@celery_app.task(
    bind=True,
    name="medical_rag.process_document",
    max_retries=3,
    default_retry_delay=10,
)
def process_document_task(self, document_id: str, job_id: str):
    db = SessionLocal()
    repo = BackgroundJobRepository(db)
    try:
        repo.update_status(job_id, JobStatus.RUNNING, task_id=self.request.id)

        # Connect your existing document pipeline logic here

        repo.update_status(job_id, JobStatus.COMPLETED, progress=1.0)
    except Exception as exc:
        attempt = self.request.retries + 1
        if attempt < self.max_retries:
            repo.update_status(
                job_id, JobStatus.RETRY, attempt_count=attempt, error_message=str(exc)
            )
            raise self.retry(exc=exc)
        else:
            repo.update_status(
                job_id,
                JobStatus.FAILED,
                attempt_count=attempt,
                error_code="PROCESSING_ERROR",
                error_message=str(exc),
            )
    finally:
        db.close()
