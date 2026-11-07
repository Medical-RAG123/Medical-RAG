import asyncio

import numpy as np
from app.api.ai.vectorstore.faiss_store import FAISSVectorStore
from app.config.settings import settings


async def main():
    # 1. Create FAISS vector store
    vector_store = FAISSVectorStore()

    # 2. Create/load the collection
    await vector_store.create_collection()

    # 3. Get embedding dimension from settings
    dimension = settings.embedding_dimension

    # 4. Create 3 test vectors
    vectors = np.random.rand(
        3,
        dimension,
    ).astype("float32")

    # 5. Create metadata for the vectors
    payloads = [
        {
            "id": "vector-1",
            "chunk_id": "chunk-1",
            "document_id": "document-1",
            "content": "Diabetes is a medical condition.",
            "metadata": {},
        },
        {
            "id": "vector-2",
            "chunk_id": "chunk-2",
            "document_id": "document-1",
            "content": "Fever is an increase in body temperature.",
            "metadata": {},
        },
        {
            "id": "vector-3",
            "chunk_id": "chunk-3",
            "document_id": "document-2",
            "content": "Heart disease affects the heart.",
            "metadata": {},
        },
    ]

    # 6. Insert the vectors
    await vector_store.upsert(
        vectors=vectors,
        payloads=payloads,
    )

    # 7. Print before deletion
    print("\n----- BEFORE DELETION -----")
    print("Metadata count:", len(vector_store.metadata))
    print("FAISS vector count:", vector_store.index.ntotal)

    for item in vector_store.metadata:
        print(item["id"], "-", item["content"])

    # 8. Delete vector-2
    await vector_store.delete(ids=["vector-2"])

    # 9. Print after deletion
    print("\n----- AFTER DELETION -----")
    print("Metadata count:", len(vector_store.metadata))
    print("FAISS vector count:", vector_store.index.ntotal)

    for item in vector_store.metadata:
        print(item["id"], "-", item["content"])


if __name__ == "__main__":
    asyncio.run(main())
