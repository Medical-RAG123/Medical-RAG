from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/profile")
def get_profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }
