import logging

logger = logging.getLogger("medical-rag")


class VectorStoreFactory:
    @staticmethod
    def create():
        """
        Creates and returns the VectorStore instance.
        """
        try:
            from app.ai.vectorstore.vector_store import VectorStore

            return VectorStore()
        except ImportError:
            from app.ai.vectorstore.chroma import ChromaVectorStore

            return ChromaVectorStore()
