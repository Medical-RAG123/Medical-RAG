class Chunker:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> list[str]:

        if not text:
            return []

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size

            chunk = text[start:end]

            if chunk.strip():
                chunks.append(chunk.strip())

            start = end - self.chunk_overlap

        return chunks
