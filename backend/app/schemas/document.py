from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime


class DocumentList(BaseModel):
    documents: list[DocumentResponse]
    total: int


class DocumentMetadata(BaseModel):
    id: str
    filename: str
