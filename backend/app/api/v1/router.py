from app.api.v1.admin import router as admin_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
