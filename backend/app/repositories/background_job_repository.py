from datetime import datetime

from sqlalchemy.orm import Session

from app.models.background_job import BackgroundJob, JobStatus


class BackgroundJobRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, job_id: str):
        return self.db.query(BackgroundJob).filter(BackgroundJob.id == job_id).first()

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        task_id: str = None,
        progress: float = None,
        error_message: str = None,
    ):
        job = self.get_by_id(job_id)

        if job is None:
            raise ValueError(f"Background job not found: {job_id}")

        job.status = status

        if task_id is not None:
            job.task_id = task_id

        if progress is not None:
            job.progress = progress

        if error_message is not None:
            job.error_message = error_message

        now = datetime.utcnow()

        if status == JobStatus.RUNNING:
            if job.started_at is None:
                job.started_at = now

        if status in (
            JobStatus.COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        ):
            job.completed_at = now

        self.db.commit()
        self.db.refresh(job)

        return job
