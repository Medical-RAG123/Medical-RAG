def build_context(results, max_tokens=None):
    parts = []
    token_count = 0

    for i, result in enumerate(results, start=1):
        content = result.content
        source = f"[Source {i}]\n{content}"

        source_tokens = source.split()

        if max_tokens is not None:
            remaining_tokens = max_tokens - token_count

            if remaining_tokens <= 0:
                break

            source_tokens = source_tokens[:remaining_tokens]
            source = " ".join(source_tokens)

        parts.append(source)
        token_count += len(source_tokens)

        if max_tokens is not None and token_count >= max_tokens:
            break

    return "\n\n".join(parts)
