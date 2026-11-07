from fastapi import APIRouter

router = APIRouter()

@router.post("")
def chat_endpoint():
    return {"response": "Mock medical response"}
