from abc import ABC, abstractmethod

from app.api.ai.retrievers.types import RetrievalResult


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        pass
