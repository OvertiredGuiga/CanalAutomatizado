"""
Configurações centralizadas da aplicação FastAPI.
Todas as configurações são lidas do arquivo .env.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


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
    
    # YouTube Data API Keys (múltiplas para fallback)
    youtube_api_key: str = ""
    youtube_api_key_2: str = ""
    youtube_api_key_3: str = ""
    youtube_api_key_4: str = ""
    
    # OpenAI API Keys (múltiplas para fallback)
    openai_api_key: str = ""
    openai_api_key_2: str = ""
    openai_api_key_3: str = ""
    openai_api_key_4: str = ""
    
    # RapidAPI Key
    rapidapi_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_openai_keys(self) -> List[str]:
        """Retorna lista de chaves OpenAI disponíveis."""
        keys = [
            self.openai_api_key,
            self.openai_api_key_2,
            self.openai_api_key_3,
            self.openai_api_key_4,
        ]
        return [key for key in keys if key]  # Filtrar vazias
    
    def get_youtube_keys(self) -> List[str]:
        """Retorna lista de chaves YouTube disponíveis."""
        keys = [
            self.youtube_api_key,
            self.youtube_api_key_2,
            self.youtube_api_key_3,
            self.youtube_api_key_4,
        ]
        return [key for key in keys if key]  # Filtrar vazias


@lru_cache()
def get_settings() -> Settings:
    """Retorna a instância única de Settings."""
    return Settings()
