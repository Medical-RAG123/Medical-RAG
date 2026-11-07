from app.api.ai.retrievers.base import Retriever
from app.api.ai.retrievers.types import RetrievalResult


class SemanticRetriever(Retriever):
    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    async def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:

        # Convert query into embedding
        query_embedding = self.embedding_service.embed_query(query)

        # Search vector store
        search_results = await self.vector_store.search(query_embedding, top_k=top_k)

        # Convert results into RetrievalResult
        results = []

        for rank, result in enumerate(search_results, start=1):
            results.append(
                RetrievalResult(
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    content=result.content,
                    metadata=result.metadata,
                    score=result.score,
                    retrieval_method="semantic",
                    rank=rank,
                )
            )

        return results
