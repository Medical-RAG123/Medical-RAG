from pydantic import BaseModel, Field


class EvaluationExample(BaseModel):
    """One question and its expected relevant retrieval results."""

    query: str = Field(min_length=1)
    relevant_chunk_ids: list[str] = Field(min_length=1)
    relevant_document_ids: list[str] = Field(default_factory=list)


class EvaluationDataset(BaseModel):
    """Collection of examples used to evaluate retrieval quality."""

    name: str = Field(min_length=1)
    version: str = "1.0"
    examples: list[EvaluationExample] = Field(min_length=1)
