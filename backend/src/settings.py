"""
Configurações centralizadas da aplicação FastAPI.
Todas as configurações são lidas do arquivo .env.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # FastAPI
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    fastapi_debug: bool = True
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # YouTube Channels
    getv_channel_id: str = "UCXXXXXXXXXXXXXXXXXXXXXXXx"
    cazetv_channel_id: str = "UCYYYYYYYYYYYYYYYYYYYYYYYy"
    
    # OpenAI (optional)
    openai_api_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Retorna a instância única de Settings."""
    return Settings()
