from app.api.ai.evaluation.metrics import precision_at_k

retrieved = [
    "test001",
    "test003",
    "test004",
]

relevant = [
    "test001",
]

score = precision_at_k(
    retrieved_chunk_ids=retrieved,
    relevant_chunk_ids=relevant,
    k=3,
)

print("Retrieved:", retrieved)
print("Relevant:", relevant)
print("K:", 3)
print("Precision@3:", score)
