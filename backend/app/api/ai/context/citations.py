def generate_citation_id(index: int) -> str:
    return f"CIT-{index}"

def map_citations(results):
    citations = []
    for index, result in enumerate(results, start=1):
        citations.append(
            {
                "citation_id": generate_citation_id(index),
                "content": result.content,
            }
        )
    return citations
