from typing import Any
from uuid import NAMESPACE_URL, uuid5

from app.api.ai.vectorstore.base import VectorStore
from app.api.ai.vectorstore.types import SearchResult
from app.config.settings import settings
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointIdsList,
    PointStruct,
    VectorParams,
)


class QdrantVectorStore(VectorStore):
    def __init__(self) -> None:
        if not settings.qdrant_url:
            raise ValueError("QDRANT_URL is not configured in the .env file.")

        self.client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

        self.collection_name = settings.vector_collection_name

    def _get_distance(self) -> Distance:
        if settings.vector_distance.lower() == "cosine":
            return Distance.COSINE

        if settings.vector_distance.lower() == "euclidean":
            return Distance.EUCLID

        if settings.vector_distance.lower() == "dot":
            return Distance.DOT

        raise ValueError(f"Unsupported vector distance: {settings.vector_distance}")

    def _get_point_id(self, payload: dict[str, Any]) -> str:
        original_id = str(payload.get("id", ""))

        if not original_id:
            raise ValueError("Payload must contain an 'id' field.")

        return str(uuid5(NAMESPACE_URL, original_id))

    async def create_collection(self) -> None:
        exists = await self.client.collection_exists(
            collection_name=self.collection_name
        )

        if exists:
            return

        await self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=settings.embedding_dimension,
                distance=self._get_distance(),
            ),
        )

    async def upsert(
        self,
        vectors,
        payloads,
    ) -> None:
        await self.create_collection()

        if len(vectors) != len(payloads):
            raise ValueError("The number of vectors must match the number of payloads.")

        points = []

        for vector, payload in zip(vectors, payloads):
            point_id = self._get_point_id(payload)

            points.append(
                PointStruct(
                    id=point_id,
                    vector=list(vector),
                    payload=payload,
                )
            )

        if points:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

    async def search(
        self,
        query_vector,
        top_k: int,
        filters=None,
    ) -> list[SearchResult]:

        await self.create_collection()

        response = await self.client.query_points(
            collection_name=self.collection_name,
            query=list(query_vector),
            limit=top_k,
            query_filter=filters,
        )

        results: list[SearchResult] = []

        for point in response.points:
            payload = point.payload or {}

            results.append(
                SearchResult(
                    id=str(payload.get("id", point.id)),
                    score=float(point.score),
                    chunk_id=str(payload.get("chunk_id", "")),
                    document_id=str(payload.get("document_id", "")),
                    content=str(payload.get("content", "")),
                    metadata=payload.get(
                        "metadata",
                        {},
                    ),
                )
            )

        return results

    async def delete(
        self,
        ids,
    ) -> None:

        await self.create_collection()

        point_ids = [str(uuid5(NAMESPACE_URL, str(item))) for item in ids]

        if not point_ids:
            return

        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=PointIdsList(
                points=point_ids,
            ),
        )

    async def delete_by_document(
        self,
        document_id,
    ) -> None:

        await self.create_collection()

        document_filter = Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=str(document_id)),
                )
            ]
        )

        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=document_filter,
        )
