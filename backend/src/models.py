"""
Modelos Pydantic para validação de requisições e respostas.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class ModeEnum(str, Enum):
    """Enum para os modos de coleta."""
    MANUAL = "manual"
    AUTO = "auto"


class FilterByEnum(str, Enum):
    """Enum para filtros de busca."""
    RELEVANCE = "relevance"
    DATE = "date"


class TimeRangeEnum(str, Enum):
    """Enum para intervalos de tempo."""
    ANY = "any"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class CollectRequest(BaseModel):
    """Modelo para requisição de coleta de vídeos."""
    
    mode: ModeEnum = Field(default=ModeEnum.MANUAL, description="Modo de coleta: 'manual' ou 'auto'")
    search_query: Optional[str] = Field(default="", description="Query de busca (apenas para modo manual)")
    channel_ids: Optional[List[str]] = Field(default=None, description="IDs de canais para filtrar")
    filter_by: FilterByEnum = Field(default=FilterByEnum.RELEVANCE, description="Filtro de busca")
    time_range: TimeRangeEnum = Field(default=TimeRangeEnum.ANY, description="Intervalo de tempo")
    max_duration: Optional[int] = Field(default=None, description="Duração máxima em minutos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "mode": "manual",
                "search_query": "Flamengo",
                "channel_ids": ["UCxxx", "UCyyy"],
                "filter_by": "date",
                "time_range": "week",
                "max_duration": 120
            }
        }


class VideoInfo(BaseModel):
    """Modelo para informações de um vídeo."""
    
    video_id: str
    title: str
    channel: Optional[str] = None
    duration: Optional[int] = None
    upload_date: Optional[str] = None
    url: str


class CollectResponse(BaseModel):
    """Modelo para resposta de coleta."""
    
    task_id: str = Field(description="ID da tarefa Celery")
    status: str = Field(description="Status da tarefa")
    message: str = Field(description="Mensagem descritiva")


class TaskStatusResponse(BaseModel):
    """Modelo para resposta de status da tarefa."""
    
    task_id: str = Field(description="ID da tarefa")
    status: str = Field(description="Status atual da tarefa")
    result: Optional[dict] = Field(default=None, description="Resultado da tarefa")
    error: Optional[str] = Field(default=None, description="Mensagem de erro se houver")
    progress: Optional[dict] = Field(default=None, description="Informações de progresso")
