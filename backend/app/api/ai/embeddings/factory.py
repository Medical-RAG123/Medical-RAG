from app.api.ai.embeddings.gemini import GeminiEmbeddingProvider
from app.config.settings import settings


def get_embedding_provider():

    if settings.embedding_provider == "google":
        return GeminiEmbeddingProvider(
            api_key=settings.gemini_api_key,
            model=settings.embedding_model,
            dimension=settings.embedding_dimension,
        )

    elif settings.embedding_provider == "sentence_transformers":
        from app.api.ai.embeddings.sentence_transformers import (
            SentenceTransformerEmbeddingProvider,
        )

        return SentenceTransformerEmbeddingProvider()

    else:
        raise ValueError(
            f"Unsupported embedding provider: {settings.embedding_provider}"
        )
