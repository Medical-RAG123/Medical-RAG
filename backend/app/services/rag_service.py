import asyncio
import inspect
import logging

logger = logging.getLogger(__name__)

class RagService:
    async def answer_question(self, question: str):
        return {"answer": "Sample answer", "citations": []}
