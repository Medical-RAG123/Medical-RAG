class EmbeddingService:
    def _init_(self, embedding_provider):
        self.embedding_provider = embedding_provider

    def embed_chunks(self, chunks):
        texts = [chunk.text for chunk in chunks]

        embeddings = self.embedding_provider.embed(texts)

        results = []

        for chunk, embedding in zip(chunks, embeddings):
            results.append(
                {"chunk_id": chunk.id, "text": chunk.text, "embedding": embedding}
            )

        return results
