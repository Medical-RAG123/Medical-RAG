from app.api.ai.retrievers.factory import RetrieverFactory
from app.api.ai.retrievers.types import RetrievalResult


class DummyEmbeddingService:
    def embed_query(self, query):
        return [0.1, 0.2, 0.3]


class DummyVectorStore:
    def search(self, query_embedding, top_k=20):

        return [
            RetrievalResult(
                chunk_id="test001",
                document_id="doc001",
                content="Metformin is commonly used to control blood glucose levels. Common side effects may include nausea and diarrhea.",
                metadata={"source": "diabetes.pdf", "document_type": "medical"},
                score=0.95,
                retrieval_method="semantic",
                rank=1,
            ),
            RetrievalResult(
                chunk_id="test003",
                document_id="doc003",
                content="Insulin is a hormone that helps control blood sugar levels in people with diabetes.",
                metadata={"source": "diabetes2.pdf", "document_type": "medical"},
                score=0.80,
                retrieval_method="semantic",
                rank=2,
            ),
        ]


if __name__ == "__main__":
    embedding_service = DummyEmbeddingService()
    vector_store = DummyVectorStore()

    retriever = RetrieverFactory.create(embedding_service, vector_store)

    print("Retriever factory created successfully!")
    print("Retriever type:", type(retriever).__name__)

    print("\nTesting real Hybrid Retriever pipeline...")

    results = retriever.retrieve("metformin side effects", top_k=3)

    print("\n===== REAL FACTORY PIPELINE TEST =====")

    for result in results:
        print("\n--- Result ---")
        print("Rank:", result.rank)
        print("Chunk ID:", result.chunk_id)
        print("Document ID:", result.document_id)
        print("Score:", result.score)
        print("Method:", result.retrieval_method)
        print("Source:", result.metadata.get("source"))
        print("Content:", result.content)

    print("\nFactory pipeline test completed successfully!")
