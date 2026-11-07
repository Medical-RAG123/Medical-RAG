import asyncio

import numpy as np
from app.api.ai.vectorstore.faiss_store import FAISSVectorStore
from app.config.settings import settings


async def main():
    # Create FAISS vector store
    vector_store = FAISSVectorStore()

    # Create/load collection
    await vector_store.create_collection()

    # Get embedding dimension
    dimension = settings.embedding_dimension

    # Create three test vectors
    vectors = np.random.rand(
        3,
        dimension,
    ).astype("float32")

    # Create test data
    payloads = [
        {
            "id": "vector-1",
            "chunk_id": "chunk-1",
            "document_id": "document-1",
            "content": "Diabetes information.",
            "metadata": {},
        },
        {
            "id": "vector-2",
            "chunk_id": "chunk-2",
            "document_id": "document-1",
            "content": "Fever information.",
            "metadata": {},
        },
        {
            "id": "vector-3",
            "chunk_id": "chunk-3",
            "document_id": "document-2",
            "content": "Heart disease information.",
            "metadata": {},
        },
    ]

    # Insert vectors
    await vector_store.upsert(
        vectors=vectors,
        payloads=payloads,
    )

    # Print before deletion
    print("\n----- BEFORE DOCUMENT DELETION -----")
    print("Metadata count:", len(vector_store.metadata))
    print("FAISS vector count:", vector_store.index.ntotal)

    for item in vector_store.metadata:
        print(
            item["document_id"],
            "-",
            item["content"],
        )

    # Delete document-1 and all its vectors
    await vector_store.delete_by_document(document_id="document-1")

    # Print after deletion
    print("\n----- AFTER DOCUMENT DELETION -----")
    print("Metadata count:", len(vector_store.metadata))
    print("FAISS vector count:", vector_store.index.ntotal)

    for item in vector_store.metadata:
        print(
            item["document_id"],
            "-",
            item["content"],
        )


if __name__ == "__main__":
    asyncio.run(main())
