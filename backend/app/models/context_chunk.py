class ContextChunk:
    def __init__(
        self,
        chunk_id: str,
        content: str,
        document_id: str,
        filename: str,
        page_number: int | None,
        section: str | None,
        score: float,
        citation_id: str,
    ):
        self.chunk_id = chunk_id
        self.content = content
        self.document_id = document_id
        self.filename = filename
        self.page_number = page_number
        self.section = section
        self.score = score
        self.citation_id = citation_id
