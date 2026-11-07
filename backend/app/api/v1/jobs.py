from datetime import datetime

from app.database import get_db
from app.services.background_job_service import BackgroundJobService
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import your authentication dependency here (e.g., get_current_user)

router = APIRouter(prefix="/api/v1/jobs", tags=["Background Jobs"])


class JobResponse(BaseModel):
    id: str
    task_id: str | None
    job_type: str
    status: str
    progress: float
    attempt_count: int
    error_code: str | None
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

    class Config:
        from_attributes = True


@router.get("/{job_id}", response_model=JobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    service = BackgroundJobService(db)
    # Replace "current-user-id" with your actual auth dependency
    job = service.get_job_status(job_id, user_id="current-user-id", is_admin=True)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found or unauthorized",
        )
    return job
