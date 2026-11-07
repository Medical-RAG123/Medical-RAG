import asyncio

from app.api.ai.vectorstore.qdrant_store import QdrantVectorStore


async def main():
    store = QdrantVectorStore()

    print("Creating Qdrant collection...")

    await store.create_collection()

    print("Collection creation completed!")


asyncio.run(main())
