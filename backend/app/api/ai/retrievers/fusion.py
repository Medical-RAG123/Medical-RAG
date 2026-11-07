from app.api.ai.retrievers.types import RetrievalResult


class RRFFusion:
    def __init__(self, k: int = 60):
        self.k = k

    def fuse(self, result_lists: list[list[RetrievalResult]]) -> list[RetrievalResult]:

        scores = {}
        results_by_chunk = {}

        for results in result_lists:
            for rank, result in enumerate(results, start=1):
                chunk_id = result.chunk_id

                # Store the result
                results_by_chunk[chunk_id] = result

                # Calculate RRF score
                rrf_score = 1 / (self.k + rank)

                scores[chunk_id] = scores.get(chunk_id, 0) + rrf_score

        # Sort by combined RRF score
        sorted_chunk_ids = sorted(scores, key=scores.get, reverse=True)

        fused_results = []

        for rank, chunk_id in enumerate(sorted_chunk_ids, start=1):
            original_result = results_by_chunk[chunk_id]

            fused_results.append(
                RetrievalResult(
                    chunk_id=original_result.chunk_id,
                    document_id=original_result.document_id,
                    content=original_result.content,
                    metadata=original_result.metadata,
                    score=scores[chunk_id],
                    retrieval_method="hybrid",
                    rank=rank,
                )
            )

        return fused_results
