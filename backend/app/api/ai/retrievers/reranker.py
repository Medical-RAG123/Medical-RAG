from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, results):
        if not results:
            return []

        # Save the original rank before reranking
        for result in results:
            result.original_rank = result.rank

        pairs = [(query, result.content) for result in results]

        scores = self.model.predict(pairs)

        for result, score in zip(results, scores):
            result.score = float(score)
            result.retrieval_method = "reranker"

        results.sort(key=lambda result: result.score, reverse=True)

        # Assign new rank after reranking
        for rank, result in enumerate(results, start=1):
            result.rank = rank

        return results
