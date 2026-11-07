import math


def precision_at_k(
    retrieved_chunk_ids: list[str], relevant_chunk_ids: list[str], k: int
) -> float:

    if k <= 0:
        return 0.0

    top_k = retrieved_chunk_ids[:k]

    if not top_k:
        return 0.0

    relevant_count = sum(1 for chunk_id in top_k if chunk_id in relevant_chunk_ids)

    return relevant_count / len(top_k)


def recall_at_k(
    retrieved_chunk_ids: list[str], relevant_chunk_ids: list[str], k: int
) -> float:

    if k <= 0:
        return 0.0

    top_k = retrieved_chunk_ids[:k]

    if not relevant_chunk_ids:
        return 0.0

    relevant_count = sum(1 for chunk_id in relevant_chunk_ids if chunk_id in top_k)

    return relevant_count / len(relevant_chunk_ids)


def mean_reciprocal_rank(
    retrieved_lists: list[list[str]], relevant_chunk_ids: list[str]
) -> float:

    if not retrieved_lists:
        return 0.0

    if not relevant_chunk_ids:
        return 0.0

    reciprocal_ranks = []

    for retrieved in retrieved_lists:
        reciprocal_rank = 0.0

        for rank, chunk_id in enumerate(retrieved, start=1):
            if chunk_id in relevant_chunk_ids:
                reciprocal_rank = 1 / rank

                break

        reciprocal_ranks.append(reciprocal_rank)

    return sum(reciprocal_ranks) / len(reciprocal_ranks)


def ndcg_at_k(
    retrieved_chunk_ids: list[str], relevant_chunk_ids: list[str], k: int
) -> float:

    if k <= 0:
        return 0.0

    if not relevant_chunk_ids:
        return 0.0

    top_k = retrieved_chunk_ids[:k]

    if not top_k:
        return 0.0

    # Calculate DCG
    dcg = 0.0

    for rank, chunk_id in enumerate(top_k, start=1):
        if chunk_id in relevant_chunk_ids:
            relevance = 1
        else:
            relevance = 0

        dcg += relevance / math.log2(rank + 1)

    # Calculate IDCG
    ideal_relevant_count = min(len(relevant_chunk_ids), k)

    idcg = 0.0

    for rank in range(1, ideal_relevant_count + 1):
        idcg += 1 / math.log2(rank + 1)

    if idcg == 0:
        return 0.0

    # Normalize DCG
    return dcg / idcg
