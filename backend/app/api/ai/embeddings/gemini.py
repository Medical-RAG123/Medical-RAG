from app.api.ai.embeddings.types import EmbeddingResult
from google import genai


class GeminiEmbeddingProvider:
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-embedding-2",
        dimension: int = 768,
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.dimension = dimension

    def embed(self, text: str) -> EmbeddingResult:

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config={"output_dimensionality": self.dimension},
        )

        vector = response.embeddings[0].values

        return EmbeddingResult(
            vector=vector,
            provider="gemini",
            model=self.model,
            dimension=self.dimension,
        )

    def embed_query(self, text: str) -> list[float]:
        result = self.embed(text)
        return result.vector

    def embed_batch(self, texts: list[str]) -> list[EmbeddingResult]:

        response = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config={"output_dimensionality": self.dimension},
        )

        results = []

        for embedding in response.embeddings:
            results.append(
                EmbeddingResult(
                    vector=embedding.values,
                    provider="gemini",
                    model=self.model,
                    dimension=self.dimension,
                )
            )

        return results
