from app.api.ai.retrievers.deduplication import Deduplicator
from app.api.ai.retrievers.types import RetrievalResult


def make_result(chunk_id, content, rank):
    return RetrievalResult(
        chunk_id=chunk_id,
        document_id="doc1",
        content=content,
        metadata={},
        score=1.0,
        retrieval_method="hybrid",
        rank=rank,
    )


results = [
    make_result("chunk-1", "Diabetes affects blood sugar levels.", 1),
    make_result("chunk-1", "Diabetes affects blood sugar levels.", 2),
    make_result("chunk-2", "Diabetes can cause high blood glucose.", 3),
]

deduplicator = Deduplicator()

deduplicated = deduplicator.deduplicate(results)

print("Original results:", len(results))
print("After deduplication:", len(deduplicated))

for result in deduplicated:
    print(
        "Rank:",
        result.rank,
        "| Chunk ID:",
        result.chunk_id,
        "| Content:",
        result.content,
    )
