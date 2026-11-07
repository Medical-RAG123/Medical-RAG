from app.auth.dependencies import require_admin
from app.database import get_db
from app.models.user import User
from app.schemas.document import (
    DocumentResponse,
    DocumentUploadResponse,
)
from app.services.document_service import DocumentService
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    document = await DocumentService.upload_document(
        db=db,
        file=file,
        uploaded_by=current_user.id,
    )

    return {
        "message": "Document uploaded successfully",
        "document": DocumentResponse.model_validate(document),
    }
