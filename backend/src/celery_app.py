"""
Configuração centralizada do Celery.
"""

from celery import Celery
from src.settings import get_settings

settings = get_settings()

# Criar instância do Celery
celery_app = Celery(
    'flamengo_ai_creator',
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configurações adicionais do Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
)

# Auto-discover tasks
celery_app.autodiscover_tasks(['src'])
