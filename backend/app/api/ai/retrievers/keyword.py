import json
import re
from pathlib import Path

from app.api.ai.retrievers.base import Retriever
from app.api.ai.retrievers.types import RetrievalResult
from rank_bm25 import BM25Okapi


class KeywordRetriever(Retriever):
    # Convert text into clean lowercase words
    @staticmethod
    def tokenize(text: str) -> list[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def __init__(self, corpus_path: str):

        # Store the corpus file path
        self.corpus_path = Path(corpus_path)

        # Load the BM25 corpus
        with open(self.corpus_path, "r", encoding="utf-8") as file:
            self.documents = json.load(file)

        # Tokenize every document
        tokenized_documents = [
            self.tokenize(document["content"]) for document in self.documents
        ]

        # Create BM25 index
        self.bm25 = BM25Okapi(tokenized_documents)

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:

        # Tokenize the search query
        query_tokens = self.tokenize(query)

        # Calculate BM25 scores
        scores = self.bm25.get_scores(query_tokens)

        # Sort documents by score
        ranked_indexes = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:top_k]

        results = []

        # Create RetrievalResult objects
        for rank, index in enumerate(ranked_indexes, start=1):
            document = self.documents[index]

            results.append(
                RetrievalResult(
                    chunk_id=document["chunk_id"],
                    document_id=document["document_id"],
                    content=document["content"],
                    metadata=document.get("metadata", {}),
                    score=float(scores[index]),
                    retrieval_method="keyword",
                    rank=rank,
                )
            )

        return results

    def save_corpus(self, output_path: str):

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(self.documents, file, indent=4, ensure_ascii=False)

    @staticmethod
    def build_corpus(chunks, output_path: str):

        corpus = []

        for chunk in chunks:
            corpus.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "content": chunk["content"],
                    "metadata": chunk.get("metadata", {}),
                }
            )

        output_file = Path(output_path)

        # Create the folder if it does not exist
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save the corpus
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(corpus, file, indent=4, ensure_ascii=False)


# Simple test
if __name__ == "__main__":
    corpus_path = "data/keywordstore/bm25_corpus.json"

    # Create Keyword Retriever
    retriever = KeywordRetriever(corpus_path)

    # Search query
    results = retriever.retrieve("metformin side effects", top_k=5)

    # Display results
    for result in results:
        print("\n--- Result ---")
        print("Rank:", result.rank)
        print("Chunk ID:", result.chunk_id)
        print("Document ID:", result.document_id)
        print("Score:", result.score)
        print("Method:", result.retrieval_method)
        print("Content:", result.content)
