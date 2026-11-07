from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbeddingProvider:
    def __init__(
        self,
        model: str = "all-MiniLM-L6-v2",
        dimension: int | None = None,
    ):
        self.model = SentenceTransformer(model)
        self.dimension = dimension

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(text)

        return embedding.tolist()
