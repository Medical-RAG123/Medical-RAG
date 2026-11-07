from app.repositories.background_job_repository import BackgroundJobRepository

class BackgroundJobService:
    def __init__(self, db):
        self.repo = BackgroundJobRepository(db)

    def get_status(self, job_id: str):
        return self.repo.get_by_id(job_id)
