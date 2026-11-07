from app.api.ai.evaluation.metrics import recall_at_k

retrieved = [
    "test001",
    "test003",
    "test004",
]

relevant = [
    "test001",
    "test004",
]

score = recall_at_k(
    retrieved_chunk_ids=retrieved,
    relevant_chunk_ids=relevant,
    k=3,
)

print("Retrieved:", retrieved)
print("Relevant:", relevant)
print("K:", 3)
print("Recall@3:", score)
