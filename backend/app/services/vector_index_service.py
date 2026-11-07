from typing import Any

from app.api.ai.vectorstore.factory import VectorStoreFactory


class VectorIndexService:
    def __init__(self, embedding_service) -> None:
        self.embedding_service = embedding_service
        self.vector_store = VectorStoreFactory.create()

    async def index(
        self,
        chunks: list[str],
        document_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:

        if not chunks:
            return

        # Delete old vectors belonging to this document
        await self.vector_store.delete_by_document(document_id)

        # Create embeddings for the new chunks
        vectors = await self.embedding_service.embed_documents(chunks)

        payloads = []

        for index, chunk in enumerate(chunks):
            payload = {
                "id": f"{document_id}_{index}",
                "chunk_id": f"{document_id}_{index}",
                "document_id": document_id,
                "content": chunk,
                "metadata": metadata or {},
            }

            payloads.append(payload)

        # Store the new vectors
        await self.vector_store.upsert(
            vectors=vectors,
            payloads=payloads,
        )
