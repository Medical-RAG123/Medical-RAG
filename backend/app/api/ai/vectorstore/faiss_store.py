import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from app.api.ai.vectorstore.base import VectorStore
from app.api.ai.vectorstore.types import SearchResult
from app.config.settings import settings


class FAISSVectorStore(VectorStore):
    def __init__(self) -> None:
        self.index_path = Path(settings.faiss_index_path)
        self.metadata_path = Path(settings.faiss_metadata_path)

        self.index = None
        self.metadata: list[dict[str, Any]] = []

    async def create_collection(self) -> None:

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.index_path.exists() and self.index_path.stat().st_size > 0:
            self.index = faiss.read_index(str(self.index_path))
        else:
            dimension = settings.embedding_dimension

            if settings.vector_distance.lower() == "cosine":
                self.index = faiss.IndexFlatIP(dimension)
            else:
                self.index = faiss.IndexFlatL2(dimension)

        if self.metadata_path.exists() and self.metadata_path.stat().st_size > 0:
            with self.metadata_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                self.metadata = json.load(file)
        else:
            self.metadata = []

    async def upsert(
        self,
        vectors,
        payloads,
    ) -> None:

        if self.index is None:
            await self.create_collection()

        vectors_array = np.asarray(
            vectors,
            dtype="float32",
        )

        if settings.vector_distance.lower() == "cosine":
            faiss.normalize_L2(vectors_array)

        self.index.add(vectors_array)

        self.metadata.extend(payloads)

        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        self.metadata_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.metadata_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.metadata,
                file,
                ensure_ascii=False,
                indent=2,
            )

    async def search(
        self,
        query_vector,
        top_k: int,
        filters=None,
    ) -> list[SearchResult]:

        if self.index is None:
            await self.create_collection()

        query = np.asarray(
            [query_vector],
            dtype="float32",
        )

        if settings.vector_distance.lower() == "cosine":
            faiss.normalize_L2(query)

        scores, indices = self.index.search(
            query,
            top_k,
        )

        results: list[SearchResult] = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):
            if index < 0:
                continue

            if index >= len(self.metadata):
                continue

            payload = self.metadata[index]

            results.append(
                SearchResult(
                    id=str(payload.get("id", index)),
                    score=float(score),
                    chunk_id=str(
                        payload.get(
                            "chunk_id",
                            "",
                        )
                    ),
                    document_id=str(
                        payload.get(
                            "document_id",
                            "",
                        )
                    ),
                    content=str(
                        payload.get(
                            "content",
                            "",
                        )
                    ),
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

        if self.index is None:
            await self.create_collection()

        ids_to_delete = {str(item) for item in ids}

        # Find the positions of vectors
        # that should remain.
        remaining_indices = [
            index
            for index, item in enumerate(self.metadata)
            if str(item.get("id", "")) not in ids_to_delete
        ]

        # Keep the metadata for
        # the remaining vectors.
        remaining_metadata = [self.metadata[index] for index in remaining_indices]

        dimension = settings.embedding_dimension

        # Create a new empty FAISS index.
        if settings.vector_distance.lower() == "cosine":
            new_index = faiss.IndexFlatIP(dimension)
        else:
            new_index = faiss.IndexFlatL2(dimension)

        # Rebuild the new index using
        # the remaining vectors.
        if remaining_indices and self.index.ntotal > 0:
            all_vectors = self.index.reconstruct_n(
                0,
                self.index.ntotal,
            )

            remaining_vectors = all_vectors[remaining_indices]

            new_index.add(remaining_vectors)

        # Update the current index and metadata.
        self.index = new_index
        self.metadata = remaining_metadata

        # Save FAISS index.
        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        # Save metadata.
        with self.metadata_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.metadata,
                file,
                ensure_ascii=False,
                indent=2,
            )

    async def delete_by_document(
        self,
        document_id,
    ) -> None:

        if self.index is None:
            await self.create_collection()

        document_id = str(document_id)

        # Find the positions of vectors
        # that should remain.
        remaining_indices = [
            index
            for index, item in enumerate(self.metadata)
            if str(
                item.get(
                    "document_id",
                    "",
                )
            )
            != document_id
        ]

        # Keep metadata for the
        # remaining vectors.
        remaining_metadata = [self.metadata[index] for index in remaining_indices]

        dimension = settings.embedding_dimension

        # Create a new empty FAISS index.
        if settings.vector_distance.lower() == "cosine":
            new_index = faiss.IndexFlatIP(dimension)
        else:
            new_index = faiss.IndexFlatL2(dimension)

        # Rebuild the FAISS index
        # with the remaining vectors.
        if remaining_indices and self.index.ntotal > 0:
            all_vectors = self.index.reconstruct_n(
                0,
                self.index.ntotal,
            )

            remaining_vectors = all_vectors[remaining_indices]

            new_index.add(remaining_vectors)

        # Update index and metadata.
        self.index = new_index
        self.metadata = remaining_metadata

        # Save FAISS index.
        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        # Save metadata.
        with self.metadata_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.metadata,
                file,
                ensure_ascii=False,
                indent=2,
            )
