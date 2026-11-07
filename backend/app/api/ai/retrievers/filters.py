from app.api.ai.retrievers.types import RetrievalResult


class MetadataFilter:
    def filter(
        self, results: list[RetrievalResult], filters: dict | None = None
    ) -> list[RetrievalResult]:

        if not filters:
            return results

        filtered_results = []

        for result in results:
            metadata = result.metadata

            matches = True

            for key, expected_value in filters.items():
                if metadata.get(key) != expected_value:
                    matches = False
                    break

            if matches:
                filtered_results.append(result)

        # Recalculate rank after filtering
        for rank, result in enumerate(filtered_results, start=1):
            result.rank = rank

        return filtered_results
