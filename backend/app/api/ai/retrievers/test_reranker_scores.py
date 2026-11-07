from app.api.ai.retrievers.reranker import CrossEncoderReranker
from app.api.ai.retrievers.types import RetrievalResult

results = [
    RetrievalResult(
        chunk_id="chunk1",
        document_id="doc1",
        content="Diabetes is a disease related to high blood sugar levels.",
        metadata={},
        score=0.80,
        retrieval_method="semantic",
        rank=1,
    ),
    RetrievalResult(
        chunk_id="chunk2",
        document_id="doc1",
        content="Hypertension is a condition involving high blood pressure.",
        metadata={},
        score=0.70,
        retrieval_method="semantic",
        rank=2,
    ),
]


reranker = CrossEncoderReranker()

reranked_results = reranker.rerank("What is diabetes?", results)


print("\nReranking results:")

for result in reranked_results:
    print("--------------------------------")
    print("Chunk ID:", result.chunk_id)
    print("Score:", result.score)
    print("Method:", result.retrieval_method)
    print("Rank:", result.rank)
