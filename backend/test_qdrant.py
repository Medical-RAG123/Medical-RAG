import asyncio

from app.api.ai.vectorstore.qdrant_store import QdrantVectorStore
from app.config.settings import settings
from qdrant_client import QdrantClient


async def create_and_check_collection():

    # Create Qdrant Vector Store
    store = QdrantVectorStore()

    # Create collection
    await store.create_collection()

    print(f"\nCollection '{settings.vector_collection_name}' creation checked.")


asyncio.run(create_and_check_collection())


# Connect to Qdrant
client = QdrantClient(
    url=settings.qdrant_url,
)


# Get all collections
collections = client.get_collections()


print("\nAvailable Qdrant collections:")

for collection in collections.collections:
    print("-", collection.name)


# Check collection
collection_name = settings.vector_collection_name

if any(collection.name == collection_name for collection in collections.collections):
    print(f"\nSUCCESS: Collection '{collection_name}' exists! ✅")
else:
    print(f"\nCollection '{collection_name}' does not exist yet. ❌")
