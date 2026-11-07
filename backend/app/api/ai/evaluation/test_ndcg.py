from app.api.ai.evaluation.metrics import ndcg_at_k

retrieved = ["test003", "test001", "test004"]

relevant = ["test001", "test004"]

score = ndcg_at_k(retrieved_chunk_ids=retrieved, relevant_chunk_ids=relevant, k=3)

print("Retrieved:", retrieved)
print("Relevant:", relevant)
print("K:", 3)
print("NDCG@3:", score)
