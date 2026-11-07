from app.auth.dependencies import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/profile")
def get_profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
    }
