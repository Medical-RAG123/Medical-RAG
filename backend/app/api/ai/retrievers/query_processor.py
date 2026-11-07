import re


class QueryProcessor:
    def process(self, query: str) -> str:
        # Remove extra spaces
        query = re.sub(r"\s+", " ", query)

        # Remove spaces at the beginning and end
        query = query.strip()

        # Remove punctuation while keeping useful medical characters
        query = re.sub(r"[^\w\s\-/\.]", "", query)

        return query
