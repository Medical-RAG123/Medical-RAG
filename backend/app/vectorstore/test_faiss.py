import asyncio

from app.api.ai.vectorstore.faiss_store import FAISSVectorStore


async def main():
    print("Creating FAISS vector store...")

    vector_store = FAISSVectorStore()

    await vector_store.create_collection()

    print("FAISS collection created successfully.")

    # Create two test vectors.
    # Each vector must contain exactly 768 numbers.
    vector1 = [0.1] * 768
    vector2 = [0.2] * 768

    payloads = [
        {
            "id": "test-1",
            "chunk_id": "chunk-1",
            "document_id": "document-1",
            "content": "This is the first test medical document.",
            "metadata": {"source": "test"},
        },
        {
            "id": "test-2",
            "chunk_id": "chunk-2",
            "document_id": "document-2",
            "content": "This is the second test medical document.",
            "metadata": {"source": "test"},
        },
    ]

    print("Adding test vectors...")

    await vector_store.upsert(
        [vector1, vector2],
        payloads,
    )

    print("Test vectors added successfully.")

    # Search using another 768-dimensional vector.
    query_vector = [0.1] * 768

    print("Searching FAISS...")

    results = await vector_store.search(
        query_vector=query_vector,
        top_k=2,
    )
    print("Number of results:", len(results))

    print("\nSearch results:")

    for result in results:
        print("-------------------------")
        print("ID:", result.id)
        print("Score:", result.score)
        print("Chunk ID:", result.chunk_id)
        print("Document ID:", result.document_id)
        print("Content:", result.content)
        print("Metadata:", result.metadata)


if __name__ == "__main__":
    asyncio.run(main())
