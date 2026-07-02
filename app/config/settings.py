from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """项目配置"""

    # ==========================
    # App
    # ==========================
    APP_NAME: str = "Logistics Agent"
    VERSION: str = "2.0.0"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ==========================
    # Database
    # ==========================
    DATABASE_URL: str = "sqlite:///app/data/orders.db"

    # ==========================
    # DeepSeek
    # ==========================
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"

    MODEL_NAME: str = "deepseek-chat"

    # ==========================
    # RAG
    # ==========================
    EMBEDDING_MODEL: str = "BAAI/bge-small-zh-v1.5"

    VECTOR_DB: str = "faiss"

    # ==========================
    # Log
    # ==========================
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()