class EvaluatedClaim:
    claim_id: str
    text: str
    supported: bool
    supporting_citations: list[str]
    confidence: float | None
