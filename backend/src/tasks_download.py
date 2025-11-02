"""
Tarefas Celery para download de vídeos.
"""

import logging
from celery import shared_task, Task
from src.celery_app import celery_app
from src.modules.youtube_downloader import YouTubeDownloader

logger = logging.getLogger(__name__)


class DownloadTask(Task):
    """Task base para downloads com suporte a callbacks."""
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Callback ao fazer retry."""
        logger.warning(f"Download task {task_id} retrying due to {exc}")
        super().on_retry(exc, task_id, args, kwargs, einfo)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Callback ao falhar."""
        logger.error(f"Download task {task_id} failed: {exc}")
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def on_success(self, result, task_id, args, kwargs):
        """Callback ao suceder."""
        logger.info(f"Download task {task_id} succeeded")
        super().on_success(result, task_id, args, kwargs)


@celery_app.task(
    bind=True,
    base=DownloadTask,
    max_retries=2,
    default_retry_delay=30,
)
def download_youtube_video(
    self,
    video_url: str,
    format_choice: str = "best",
):
    """
    Tarefa Celery para fazer download de um vídeo do YouTube.
    
    Args:
        video_url: URL do vídeo
        format_choice: Formato desejado ('best', 'best[ext=mp4]', etc)
    
    Returns:
        Informações do download
    """
    
    try:
        # Atualizar estado da tarefa
        self.update_state(
            state='PROGRESS',
            meta={'current': 0, 'total': 100, 'status': 'Iniciando download...'}
        )
        
        # Inicializar downloader
        downloader = YouTubeDownloader(output_path="downloads")
        
        # Callback para atualizar progresso
        def progress_callback(info):
            if info.get('status') == 'downloading':
                percent_str = info.get('percent', '0%').strip('%')
                try:
                    percent = float(percent_str)
                except ValueError:
                    percent = 0
                
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'current': int(percent),
                        'total': 100,
                        'status': f"Baixando: {info.get('speed', 'N/A')} - ETA: {info.get('eta', 'N/A')}",
                        'downloaded_bytes': info.get('downloaded_bytes', 0),
                        'total_bytes': info.get('total_bytes', 0),
                    }
                )
            elif info.get('status') == 'finished':
                self.update_state(
                    state='PROGRESS',
                    meta={'current': 100, 'total': 100, 'status': 'Processando arquivo...'}
                )
        
        # Fazer download
        logger.info(f"Iniciando download: {video_url}")
        result = downloader.download_video(
            video_url=video_url,
            format_choice=format_choice,
            progress_callback=progress_callback,
        )
        
        # Atualizar estado final
        self.update_state(
            state='PROGRESS',
            meta={'current': 100, 'total': 100, 'status': 'Download concluído!'}
        )
        
        logger.info(f"Download concluído: {result.get('title')}")
        return {
            'status': 'success',
            'video_info': result,
        }
    
    except Exception as exc:
        logger.error(f"Erro no download: {str(exc)}")
        
        # Retry com backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@celery_app.task(
    bind=True,
    base=DownloadTask,
    max_retries=1,
    default_retry_delay=10,
)
def download_multiple_youtube_videos(
    self,
    video_urls: list,
    format_choice: str = "best",
):
    """
    Tarefa Celery para fazer download de múltiplos vídeos.
    
    Args:
        video_urls: Lista de URLs
        format_choice: Formato desejado
    
    Returns:
        Resultados dos downloads
    """
    
    try:
        # Inicializar downloader
        downloader = YouTubeDownloader(output_path="downloads")
        
        # Callback para atualizar progresso
        def progress_callback(info):
            if info.get('status') == 'downloading_multiple':
                current = info.get('current', 0)
                total = info.get('total', len(video_urls))
                percent = int((current / total) * 100)
                
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'current': percent,
                        'total': 100,
                        'status': f"Baixando vídeo {current}/{total}: {info.get('url', 'N/A')}",
                    }
                )
        
        # Fazer downloads
        logger.info(f"Iniciando download de {len(video_urls)} vídeos")
        results = downloader.download_multiple_videos(
            video_urls=video_urls,
            format_choice=format_choice,
            progress_callback=progress_callback,
        )
        
        # Atualizar estado final
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 100,
                'total': 100,
                'status': f"Downloads concluídos! {results['successful']} sucesso, {results['failed']} falhas",
            }
        )
        
        logger.info(f"Downloads múltiplos concluídos: {results}")
        return {
            'status': 'success',
            'results': results,
        }
    
    except Exception as exc:
        logger.error(f"Erro nos downloads múltiplos: {str(exc)}")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@celery_app.task(bind=True)
def get_video_info_task(self, video_url: str):
    """
    Tarefa Celery para obter informações de um vídeo.
    
    Args:
        video_url: URL do vídeo
    
    Returns:
        Informações do vídeo
    """
    
    try:
        downloader = YouTubeDownloader()
        info = downloader.get_video_info(video_url)
        
        return {
            'status': 'success',
            'video_info': info,
        }
    
    except Exception as exc:
        logger.error(f"Erro ao obter informações: {str(exc)}")
        raise


@celery_app.task(bind=True)
def get_available_formats_task(self, video_url: str):
    """
    Tarefa Celery para obter formatos disponíveis.
    
    Args:
        video_url: URL do vídeo
    
    Returns:
        Lista de formatos disponíveis
    """
    
    try:
        downloader = YouTubeDownloader()
        formats = downloader.get_available_formats(video_url)
        
        return {
            'status': 'success',
            'formats': formats,
        }
    
    except Exception as exc:
        logger.error(f"Erro ao obter formatos: {str(exc)}")
        raise
