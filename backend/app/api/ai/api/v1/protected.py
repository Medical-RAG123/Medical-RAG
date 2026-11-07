from app.auth.dependencies import require_admin, require_doctor
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_admin),
):
    return {
        "message": "Welcome to the admin dashboard",
        "user_id": current_user.id,
        "role": current_user.role.value,
    }


@router.get("/doctor")
def doctor_dashboard(
    current_user: User = Depends(require_doctor),
):
    return {
        "message": "Welcome to the doctor dashboard",
        "user_id": current_user.id,
        "role": current_user.role.value,
    }
