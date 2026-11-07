import asyncio

from app.api.ai.vectorstore.factory import VectorStoreFactory


async def main():
    print("Starting FAISS metadata test...")

    # Create vector store
    vector_store = VectorStoreFactory.create()
    print("Vector store created successfully.")

    # Create/load FAISS index
    await vector_store.create_collection()
    print("Collection/index created successfully.")

    # Create test vectors
    vector1 = [0.1] * 768
    vector2 = [0.2] * 768

    # Payload / metadata
    payloads = [
        {
            "id": "test-1",
            "chunk_id": "chunk-1",
            "document_id": "document-1",
            "content": "Diabetes affects blood sugar levels.",
            "metadata": {
                "source": "test1.txt",
                "file_type": "txt",
            },
        },
        {
            "id": "test-2",
            "chunk_id": "chunk-2",
            "document_id": "document-2",
            "content": "Hypertension is related to high blood pressure.",
            "metadata": {
                "source": "test2.txt",
                "file_type": "txt",
            },
        },
    ]

    # Store vectors + payloads
    await vector_store.upsert(
        vectors=[vector1, vector2],
        payloads=payloads,
    )

    print("Vector and payloads inserted successfully.")

    # Search using a test vector
    query_vector = [0.1] * 768

    results = await vector_store.search(
        query_vector=query_vector,
        top_k=2,
    )

    # Check Top-K
    print("\nNumber of results:", len(results))

    print("\nSearch Results:")
    print("-------------------------")

    for result in results:
        print("ID:", result.id)
        print("Score:", result.score)
        print("Chunk ID:", result.chunk_id)
        print("Document ID:", result.document_id)
        print("Content:", result.content)
        print("Metadata:", result.metadata)
        print("-------------------------")

    print("\nFAISS metadata and Top-K test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
