from app.api.ai.retrievers.filters import MetadataFilter
from app.api.ai.retrievers.types import RetrievalResult

results = [
    RetrievalResult(
        chunk_id="chunk1",
        document_id="doc1",
        content="Diabetes information",
        metadata={"source": "diabetes.pdf", "document_type": "medical"},
        score=0.9,
        retrieval_method="semantic",
        rank=1,
    ),
    RetrievalResult(
        chunk_id="chunk2",
        document_id="doc2",
        content="Hypertension information",
        metadata={"source": "hypertension.pdf", "document_type": "medical"},
        score=0.8,
        retrieval_method="semantic",
        rank=2,
    ),
    RetrievalResult(
        chunk_id="chunk3",
        document_id="doc3",
        content="General information",
        metadata={"source": "general.txt", "document_type": "general"},
        score=0.7,
        retrieval_method="semantic",
        rank=3,
    ),
]


metadata_filter = MetadataFilter()


filtered_results = metadata_filter.filter(results, {"document_type": "medical"})


print("\nMETADATA FILTER TEST")
print("====================")

for result in filtered_results:
    print("Chunk ID:", result.chunk_id)
    print("Document ID:", result.document_id)
    print("Metadata:", result.metadata)
    print("Rank:", result.rank)
    print("--------------------")
