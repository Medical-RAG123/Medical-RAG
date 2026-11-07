from app.api.ai.retrievers.base import Retriever
from app.api.ai.retrievers.types import RetrievalResult


class HybridRetriever(Retriever):
    def __init__(
        self,
        query_processor,
        semantic_retriever,
        keyword_retriever,
        fusion,
        deduplicator,
        metadata_filter,
        reranker,
    ):
        self.query_processor = query_processor
        self.semantic_retriever = semantic_retriever
        self.keyword_retriever = keyword_retriever
        self.fusion = fusion
        self.deduplicator = deduplicator
        self.metadata_filter = metadata_filter
        self.reranker = reranker

    async def retrieve(
        self, query: str, top_k: int = 10, filters: dict | None = None
    ) -> list[RetrievalResult]:

        # Step 1: Process query
        processed_query = self.query_processor.process(query)

        # Step 2: Semantic retrieval
        semantic_results = await self.semantic_retriever.retrieve(
            processed_query, top_k=20
        )

        # Step 3: Keyword retrieval
        keyword_results = self.keyword_retriever.retrieve(processed_query, top_k=20)

        # Step 4: RRF fusion
        fused_results = self.fusion.fuse([semantic_results, keyword_results])

        # Step 5: Remove duplicate chunks
        deduplicated_results = self.deduplicator.deduplicate(fused_results)

        # Step 6: Apply metadata filters
        filtered_results = self.metadata_filter.filter(deduplicated_results, filters)

        # Step 7: Rerank results
        reranked_results = self.reranker.rerank(processed_query, filtered_results)

        # Step 8: Return Top-K results
        return reranked_results[:top_k]
