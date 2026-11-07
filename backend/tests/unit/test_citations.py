from app.api.ai.context.citations import generate_citation_id, map_citations


def test_generate_citation_id():
    assert generate_citation_id(0) == "CIT-0"
    assert generate_citation_id(1) == "CIT-1"
    assert generate_citation_id(2) == "CIT-2"


def test_map_citations():
    results = [
        type("R", (), {"content": "Diabetes is related to high blood sugar."})(),
        type("R", (), {"content": "Insulin helps control blood glucose."})(),
    ]

    citations = map_citations(results)

    assert len(citations) == 2
    assert citations[0]["citation_id"] == "CIT-1"
    assert citations[0]["content"] == "Diabetes is related to high blood sugar."
    assert citations[1]["citation_id"] == "CIT-2"
    assert citations[1]["content"] == "Insulin helps control blood glucose."
