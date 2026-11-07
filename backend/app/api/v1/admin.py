from app.api.deps import require_admin
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/overview")
def get_admin_overview(admin=Depends(require_admin)):
    return {
        "documents": {"total": 12, "indexed": 12, "total_chunks": 145},
        "retrieval": {"status": "Healthy", "recall_at_5": 0.88},
    }
