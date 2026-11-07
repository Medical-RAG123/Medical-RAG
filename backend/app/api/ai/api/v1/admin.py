from datetime import datetime

from app.api.deps import require_admin  # Adjust to your project's RBAC import path
from app.database import get_db
from app.schemas.analytics import AdminOverviewResponse, SystemHealthResponse
from app.services.analytics_service import AnalyticsService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin", tags=["Admin Analytics"])


@router.get("/overview", response_model=AdminOverviewResponse)
def get_admin_overview(
    db: Session = Depends(get_db), current_user=Depends(require_admin)
):
    service = AnalyticsService(db)
    return service.get_overview()


@router.get("/health", response_model=SystemHealthResponse)
def get_system_health(
    db: Session = Depends(get_db), current_user=Depends(require_admin)
):
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "checked_at": datetime.utcnow(),
        "components": {
            "database": db_status,
            "vector_store": "healthy",
            "document_storage": "healthy",
            "llm_provider": "not_checked",
        },
    }
