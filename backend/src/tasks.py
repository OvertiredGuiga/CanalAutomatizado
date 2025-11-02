"""
Tarefas Celery para coleta de vídeos.
Apenas o wrapper Celery para a função de coleta.
"""

import logging
from celery import shared_task, Task
from src.celery_app import celery_app
from src.modules.youtube_collector import YouTubeCollector
from src.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CallbackTask(Task):
    """Task base com suporte a callbacks."""
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Callback ao fazer retry."""
        logger.warning(f"Task {task_id} retrying due to {exc}")
        super().on_retry(exc, task_id, args, kwargs, einfo)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Callback ao falhar."""
        logger.error(f"Task {task_id} failed: {exc}")
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def on_success(self, result, task_id, args, kwargs):
        """Callback ao suceder."""
        logger.info(f"Task {task_id} succeeded")
        super().on_success(result, task_id, args, kwargs)


@celery_app.task(
    bind=True,
    base=CallbackTask,
    max_retries=3,
    default_retry_delay=60,
)
def collect_youtube_videos(
    self,
    mode: str = "manual",
    search_query: str = "",
    channel_ids: list = None,
    filter_by: str = "relevance",
    time_range: str = "any",
    max_duration: int = None,
):
    """
    Tarefa Celery para coletar vídeos do YouTube.
    
    Args:
        mode: 'manual' ou 'auto'
        search_query: Query de busca (apenas para modo manual)
        channel_ids: Lista de IDs de canais (apenas para modo manual)
        filter_by: Filtro por 'relevance' ou 'date'
        time_range: Intervalo de tempo
        max_duration: Duração máxima em minutos
    
    Returns:
        Lista de vídeos coletados
    """
    
    try:
        # Atualizar estado da tarefa
        self.update_state(
            state='PROGRESS',
            meta={'current': 0, 'total': 100, 'status': 'Inicializando coleta...'}
        )
        
        # Inicializar o coletor
        channel_ids_dict = {
            'getv': settings.getv_channel_id,
            'cazetv': settings.cazetv_channel_id,
        }
        collector = YouTubeCollector(channel_ids_dict)
        
        # Executar coleta conforme o modo
        if mode == "auto":
            logger.info("Executando coleta automática")
            self.update_state(
                state='PROGRESS',
                meta={'current': 50, 'total': 100, 'status': 'Buscando vídeos automaticamente...'}
            )
            videos = collector.search_auto()
        else:
            logger.info(f"Executando coleta manual: {search_query}")
            self.update_state(
                state='PROGRESS',
                meta={'current': 50, 'total': 100, 'status': f'Buscando: {search_query}...'}
            )
            videos = collector.search_manual(
                search_query=search_query,
                channel_ids=channel_ids,
                filter_by=filter_by,
                time_range=time_range,
                max_duration=max_duration,
            )
        
        # Atualizar estado final
        self.update_state(
            state='PROGRESS',
            meta={'current': 100, 'total': 100, 'status': f'Coleta concluída! {len(videos)} vídeos encontrados.'}
        )
        
        logger.info(f"Coleta concluída com sucesso: {len(videos)} vídeos")
        return {
            'status': 'success',
            'total_videos': len(videos),
            'videos': videos,
        }
    
    except Exception as exc:
        logger.error(f"Erro na coleta: {str(exc)}")
        
        # Retry com backoff exponencial
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
