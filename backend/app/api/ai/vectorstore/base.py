from abc import ABC, abstractmethod

from app.api.ai.vectorstore.types import SearchResult


class VectorStore(ABC):
    @abstractmethod
    async def create_collection(self) -> None: ...

    @abstractmethod
    async def upsert(
        self,
        vectors,
        payloads,
    ) -> None: ...

    @abstractmethod
    async def search(
        self,
        query_vector,
        top_k: int,
        filters=None,
    ) -> list[SearchResult]: ...

    @abstractmethod
    async def delete(
        self,
        ids,
    ) -> None: ...

    @abstractmethod
    async def delete_by_document(
        self,
        document_id,
    ) -> None: ...
