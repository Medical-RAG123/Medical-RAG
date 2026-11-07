import time

from app.api.ai.retrievers.reranker import CrossEncoderReranker
from app.api.ai.retrievers.types import RetrievalResult

reranker = CrossEncoderReranker()

query = "What are the side effects of metformin?"

results = [
    RetrievalResult(
        chunk_id="chunk1",
        document_id="doc1",
        content="Metformin is used to control blood glucose levels.",
        metadata={},
        score=0.9,
        retrieval_method="hybrid",
        rank=1,
    ),
    RetrievalResult(
        chunk_id="chunk2",
        document_id="doc2",
        content="Paracetamol is used to reduce fever and pain.",
        metadata={},
        score=0.8,
        retrieval_method="hybrid",
        rank=2,
    ),
    RetrievalResult(
        chunk_id="chunk3",
        document_id="doc3",
        content="Common side effects of metformin include nausea and diarrhea.",
        metadata={},
        score=0.7,
        retrieval_method="hybrid",
        rank=3,
    ),
]


start_time = time.perf_counter()

reranked_results = reranker.rerank(query, results)

end_time = time.perf_counter()

latency = end_time - start_time

print("\nRERANKER RESULTS")
print("================")

for result in reranked_results:
    print("Chunk ID:", result.chunk_id)
    print("Score:", result.score)
    print("Method:", result.retrieval_method)
    print("Rank:", result.rank)
    print("Original Rank:", result.original_rank)
    print("----------------")

print("\nReranker Latency:", latency, "seconds")
