from app.api.ai.retrievers.hybrid import HybridRetriever


class DummyQueryProcessor:
    def process(self, query):
        return query.lower().strip()


class DummySemanticRetriever:
    def retrieve(self, query, top_k=20):
        from app.api.ai.retrievers.types import RetrievalResult

        return [
            RetrievalResult(
                chunk_id="test001",
                document_id="doc001",
                content="Metformin is used to control blood glucose levels.",
                metadata={"source": "diabetes.pdf"},
                score=0.95,
                retrieval_method="semantic",
                rank=1,
            ),
            RetrievalResult(
                chunk_id="test003",
                document_id="doc003",
                content="Insulin helps control blood sugar levels.",
                metadata={"source": "diabetes2.pdf"},
                score=0.80,
                retrieval_method="semantic",
                rank=2,
            ),
        ]


class DummyKeywordRetriever:
    def retrieve(self, query, top_k=20):
        from app.api.ai.retrievers.types import RetrievalResult

        return [
            RetrievalResult(
                chunk_id="test001",
                document_id="doc001",
                content="Metformin is used to control blood glucose levels.",
                metadata={"source": "diabetes.pdf"},
                score=2.9,
                retrieval_method="keyword",
                rank=1,
            ),
            RetrievalResult(
                chunk_id="test004",
                document_id="doc004",
                content="High blood pressure is also called hypertension.",
                metadata={"source": "hypertension.pdf"},
                score=1.5,
                retrieval_method="keyword",
                rank=2,
            ),
        ]


class DummyFusion:
    def fuse(self, result_lists):
        from app.api.ai.retrievers.types import RetrievalResult

        return [
            RetrievalResult(
                chunk_id="test001",
                document_id="doc001",
                content="Metformin is used to control blood glucose levels.",
                metadata={"source": "diabetes.pdf"},
                score=0.032,
                retrieval_method="hybrid",
                rank=1,
            ),
            RetrievalResult(
                chunk_id="test003",
                document_id="doc003",
                content="Insulin helps control blood sugar levels.",
                metadata={"source": "diabetes2.pdf"},
                score=0.016,
                retrieval_method="hybrid",
                rank=2,
            ),
            RetrievalResult(
                chunk_id="test004",
                document_id="doc004",
                content="High blood pressure is also called hypertension.",
                metadata={"source": "hypertension.pdf"},
                score=0.015,
                retrieval_method="hybrid",
                rank=3,
            ),
        ]


class DummyDeduplicator:
    def deduplicate(self, results):
        return results


class DummyMetadataFilter:
    def filter(self, results, filters=None):
        return results


class DummyReranker:
    def rerank(self, query, results):
        for rank, result in enumerate(results, start=1):
            result.rank = rank
            result.retrieval_method = "reranker"

        return results


query_processor = DummyQueryProcessor()
semantic_retriever = DummySemanticRetriever()
keyword_retriever = DummyKeywordRetriever()
fusion = DummyFusion()
deduplicator = DummyDeduplicator()
metadata_filter = DummyMetadataFilter()
reranker = DummyReranker()


retriever = HybridRetriever(
    query_processor,
    semantic_retriever,
    keyword_retriever,
    fusion,
    deduplicator,
    metadata_filter,
    reranker,
)


results = retriever.retrieve(
    "What are the side effects of metformin?",
    top_k=3,
)


print("\n===== HYBRID RETRIEVAL TEST =====")

for result in results:
    print("\n--- Result ---")
    print("Rank:", result.rank)
    print("Chunk ID:", result.chunk_id)
    print("Document ID:", result.document_id)
    print("Score:", result.score)
    print("Method:", result.retrieval_method)
    print("Content:", result.content)

print("\nHybrid retrieval test completed successfully!")
