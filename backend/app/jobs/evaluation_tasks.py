import structlog
from app.database import SessionLocal
from app.jobs.celery_app import celery_app
from app.models.background_job import JobStatus
from app.repositories.background_job_repository import BackgroundJobRepository

logger = structlog.get_logger()


@celery_app.task(
    bind=True,
    name="medical_rag.run_evaluation",
    max_retries=2,
)
def run_evaluation_task(self, run_id: str, job_id: str):
    db = SessionLocal()
    repo = BackgroundJobRepository(db)
    try:
        repo.update_status(
            job_id, JobStatus.RUNNING, attempt_count=self.request.retries + 1
        )
        logger.info("evaluation_run_started", run_id=run_id, job_id=job_id)

        # TODO: Integrate your Phase 19-20 evaluation runner here

        repo.update_status(job_id, JobStatus.COMPLETED, progress=100.0)
        logger.info("evaluation_run_completed", run_id=run_id, job_id=job_id)
    except Exception as exc:
        logger.error(
            "evaluation_run_failed", run_id=run_id, job_id=job_id, error=str(exc)
        )
        repo.update_status(
            job_id,
            JobStatus.RETRY
            if self.request.retries < self.max_retries
            else JobStatus.FAILED,
            error_code="EVALUATION_ERROR",
            error_message=str(exc),
        )
        raise self.retry(exc=exc, countdown=120)
    finally:
        db.close()
