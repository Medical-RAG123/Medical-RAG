from types import SimpleNamespace

from app.api.ai.context.context_builder import build_context


def test_build_context_formats_results():
    results = [
        SimpleNamespace(content="Diabetes is a chronic disease."),
        SimpleNamespace(content="Hypertension means high blood pressure."),
    ]

    context = build_context(results)

    assert context == (
        "[Source 1]\nDiabetes is a chronic disease.\n\n"
        "[Source 2]\nHypertension means high blood pressure."
    )


def test_build_context_respects_token_limit():
    results = [
        SimpleNamespace(content="Diabetes is a chronic disease. " * 100),
        SimpleNamespace(content="Hypertension means high blood pressure. " * 100),
    ]

    context = build_context(results, max_tokens=50)

    assert len(context.split()) <= 50
