from dataclasses import dataclass
from typing import Any


@dataclass
class SearchResult:
    id: str
    score: float
    chunk_id: str
    document_id: str
    content: str
    metadata: dict[str, Any]
