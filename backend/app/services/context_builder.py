def build_context(results):

    context_parts = []

    for i, result in enumerate(results, start=1):
        context_parts.append(f"[Source {i}]\n{result.content}")

    return "\n\n".join(context_parts)
