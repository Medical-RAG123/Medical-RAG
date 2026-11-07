from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Medical RAG Assistant"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    upload_directory: str
    max_upload_size_mb: int
    allowed_extensions: str

    gemini_api_key: str

    embedding_provider: str
    embedding_model: str
    embedding_dimension: int
    embedding_batch_size: int

    vector_store_provider: str
    vector_collection_name: str
    vector_distance: str
    vector_top_k: int

    faiss_index_path: str
    faiss_metadata_path: str

    qdrant_url: str | None = None
    qdrant_api_key: str | None = None

    keyword_index_path: str

    reranker_provider: str
    reranker_model: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        extra="ignore",
    )


settings = Settings()
