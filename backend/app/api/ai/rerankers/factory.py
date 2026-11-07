from app.api.ai.rerankers.cross_encoder import CrossEncoderReranker


class RerankerFactory:
    @staticmethod
    def create(provider: str):
        if provider == "cross_encoder":
            return CrossEncoderReranker()

        raise ValueError(f"Unknown reranker provider: {provider}")
