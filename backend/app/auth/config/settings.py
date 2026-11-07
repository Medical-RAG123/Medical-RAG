from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Medical RAG Assistant"
    app_version: str = "0.1.0"

    api_v1_prefix: str = "/api/v1"

    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000

    # JWT authentication settings
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
