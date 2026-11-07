from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievalResult:
    chunk_id: str
    document_id: str
    content: str
    metadata: dict[str, Any]
    score: float
    retrieval_method: str
    rank: int
    original_rank: int | None = None
