from dataclasses import dataclass


@dataclass
class EmbeddingResult:
    vector: list[float]
    provider: str
    model: str
    dimension: int
