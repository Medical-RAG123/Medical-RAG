import asyncio

from app.api.ai.vectorstore.faiss_store import FAISSVectorStore


async def main():
    store1 = FAISSVectorStore()

    await store1.create_collection()

    print("First store loaded")
    print("Vectors before:", store1.index.ntotal)

    dimension = store1.index.d

    test_vector = [0.1] * dimension

    test_payload = {
        "id": "test-persistence-1",
        "chunk_id": "chunk-1",
        "document_id": "test-document-1",
        "content": "This is a FAISS persistence test.",
        "metadata": {},
    }

    await store1.upsert(
        vectors=[test_vector],
        payloads=[test_payload],
    )

    print("Vectors after saving:", store1.index.ntotal)

    store2 = FAISSVectorStore()

    await store2.create_collection()

    print("New store loaded")
    print("Vectors after restart:", store2.index.ntotal)

    if store2.index.ntotal > 0:
        print("FAISS persistence is working successfully!")
    else:
        print("FAISS persistence failed.")


asyncio.run(main())
