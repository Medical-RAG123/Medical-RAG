import asyncio

import numpy as np
from app.services.embedding_service import EmbeddingService


def cosine_similarity(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    return np.dot(vector1, vector2) / (
        np.linalg.norm(vector1) * np.linalg.norm(vector2)
    )


async def main():
    sentences = [
        "A patient experienced a heart attack.",
        "The patient suffered a myocardial infarction.",
        "The weather is sunny today.",
    ]

    embedding_service = EmbeddingService()

    vectors = await embedding_service.embed_chunks(sentences)

    similarity_1 = cosine_similarity(vectors[0], vectors[1])
    similarity_2 = cosine_similarity(vectors[0], vectors[2])

    print("\nSemantic Similarity Results")
    print("---------------------------")

    print("\nHeart attack vs Myocardial infarction:")
    print(similarity_1)

    print("\nHeart attack vs Weather:")
    print(similarity_2)


if __name__ == "__main__":
    asyncio.run(main())
