from fastapi import FastAPI
from app.api.v1.jobs import router as jobs_router
from app.api.v1.chat import router as chat_router

app = FastAPI(title="Medical RAG API")

app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "backend-api"}
