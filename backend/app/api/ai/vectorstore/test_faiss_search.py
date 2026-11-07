import asyncio

from app.api.ai.vectorstore.factory import VectorStoreFactory


async def main():
    print("===== REAL FAISS SEARCH TEST =====")

    # Create the FAISS vector store
    vector_store = VectorStoreFactory.create()

    # Load existing FAISS index and metadata
    await vector_store.create_collection()

    print("FAISS index loaded successfully.")
    print("Number of vectors:", vector_store.index.ntotal)
    print("Number of metadata records:", len(vector_store.metadata))

    # Create a simple test query vector
    query_vector = [0.1] * 768

    # Search the existing FAISS index
    results = await vector_store.search(
        query_vector=query_vector,
        top_k=5,
    )

    print("\nNumber of results:", len(results))

    print("\nSearch Results:")
    print("-------------------------")

    for result in results:
        print("Rank:", results.index(result) + 1)
        print("Chunk ID:", result.chunk_id)
        print("Document ID:", result.document_id)
        print("Score:", result.score)
        print("Content:", result.content)
        print("Metadata:", result.metadata)
        print("-------------------------")

    print("\nReal FAISS search test completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
