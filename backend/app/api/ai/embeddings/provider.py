from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbeddingProvider:
    def __init__(
        self,
        model: str,
        dimension: int | None = None,
    ):
        self.model = SentenceTransformer(model)
        self.dimension = dimension

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(text)

        return embedding.tolist()

    from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbeddingProvider:
    def __init__(
        self,
        model: str,
        dimension: int | None = None,
    ):
        self.model = SentenceTransformer(model)
        self.dimension = dimension

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(text)

        return embedding.tolist()
