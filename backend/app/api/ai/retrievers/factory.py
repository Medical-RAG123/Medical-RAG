from app.api.ai.rerankers.factory import RerankerFactory
from app.api.ai.retrievers.deduplication import Deduplicator
from app.api.ai.retrievers.filters import MetadataFilter
from app.api.ai.retrievers.fusion import RRFFusion
from app.api.ai.retrievers.hybrid import HybridRetriever
from app.api.ai.retrievers.keyword import KeywordRetriever
from app.api.ai.retrievers.query_processor import QueryProcessor
from app.api.ai.retrievers.semantic import SemanticRetriever
from app.config.settings import settings


class RetrieverFactory:
    @staticmethod
    def create(embedding_service, vector_store):

        # Step 1: Query processor
        query_processor = QueryProcessor()

        # Step 2: Semantic retriever
        semantic_retriever = SemanticRetriever(embedding_service, vector_store)

        # Step 3: Keyword retriever
        keyword_retriever = KeywordRetriever(settings.keyword_index_path)

        # Step 4: RRF fusion
        fusion = RRFFusion(k=60)

        # Step 5: Deduplicator
        deduplicator = Deduplicator()

        # Step 6: Metadata filter
        metadata_filter = MetadataFilter()

        # Step 7: Create reranker
        reranker = RerankerFactory.create(settings.reranker_provider)

        # Step 8: Create hybrid retriever
        hybrid_retriever = HybridRetriever(
            query_processor=query_processor,
            semantic_retriever=semantic_retriever,
            keyword_retriever=keyword_retriever,
            fusion=fusion,
            deduplicator=deduplicator,
            metadata_filter=metadata_filter,
            reranker=reranker,
        )

        return hybrid_retriever
