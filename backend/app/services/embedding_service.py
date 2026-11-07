class EmbeddingService:
    def __init__(self, embedding_provider):
        self.embedding_provider = embedding_provider

    async def embed_documents(self, chunks: list[str]) -> list[list[float]]:
        """
        Generate embeddings for document chunks.
        """

        if not chunks:
            return []

        results = self.embedding_provider.embed_batch(chunks)

        return [result.vector for result in results]
