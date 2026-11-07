from app.api.ai.retrievers.fusion import RRFFusion
from app.api.ai.retrievers.types import RetrievalResult

semantic_results = [
    RetrievalResult(
        chunk_id="chunk1",
        document_id="doc1",
        content="Diabetes is related to high blood sugar.",
        metadata={},
        score=0.90,
        retrieval_method="semantic",
        rank=1,
    ),
    RetrievalResult(
        chunk_id="chunk2",
        document_id="doc1",
        content="Hypertension is related to high blood pressure.",
        metadata={},
        score=0.80,
        retrieval_method="semantic",
        rank=2,
    ),
]


keyword_results = [
    RetrievalResult(
        chunk_id="chunk2",
        document_id="doc1",
        content="Hypertension is related to high blood pressure.",
        metadata={},
        score=0.95,
        retrieval_method="keyword",
        rank=1,
    ),
    RetrievalResult(
        chunk_id="chunk3",
        document_id="doc1",
        content="Diabetes affects insulin regulation.",
        metadata={},
        score=0.70,
        retrieval_method="keyword",
        rank=2,
    ),
]


fusion = RRFFusion(k=60)


fused_results = fusion.fuse([semantic_results, keyword_results])


print("\nRRF FUSION TEST")
print("================")

for result in fused_results:
    print("Chunk ID:", result.chunk_id)
    print("RRF Score:", result.score)
    print("Method:", result.retrieval_method)
    print("Rank:", result.rank)
    print("----------------")
