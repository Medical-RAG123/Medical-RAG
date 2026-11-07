from app.api.ai.retrievers.types import RetrievalResult


class Deduplicator:
    def deduplicate(self, results: list[RetrievalResult]) -> list[RetrievalResult]:

        unique_results = {}
        seen_content = set()

        for result in results:
            # Normalize only whitespace
            content_key = " ".join(result.content.split())

            # Remove exact duplicate content
            if content_key in seen_content:
                continue

            seen_content.add(content_key)
            unique_results[result.chunk_id] = result

        deduplicated_results = list(unique_results.values())

        # Recalculate rank
        for rank, result in enumerate(deduplicated_results, start=1):
            result.rank = rank

        return deduplicated_results
