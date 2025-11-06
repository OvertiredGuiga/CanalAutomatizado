"""
Tarefas Celery para detecção de cenas em vídeos.
"""

import logging
from celery import shared_task, Task
from src.celery_app import celery_app
from src.modules.scene_detector import SceneDetector
from scenedetect.frame_timecode import FrameTimecode

logger = logging.getLogger(__name__)

class SceneDetectionTask(Task):
    """Task base para detecção de cenas com suporte a callbacks."""
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Callback ao fazer retry."""
        logger.warning(f"Scene detection task {task_id} retrying due to {exc}")
        super().on_retry(exc, task_id, args, kwargs, einfo)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Callback ao falhar."""
        logger.error(f"Scene detection task {task_id} failed: {exc}")
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def on_success(self, result, task_id, args, kwargs):
        """Callback ao suceder."""
        logger.info(f"Scene detection task {task_id} succeeded")
        super().on_success(result, task_id, args, kwargs)


@celery_app.task(
    bind=True,
    base=SceneDetectionTask,
    max_retries=1,
    default_retry_delay=10,
)
def detect_scenes_task(
    self,
    video_path: str,
    method: str = 'adaptive',
    adaptive_threshold: float = 3.0,
    content_threshold: float = 27.0,
):
    """
    Tarefa Celery para detecção de cenas em um vídeo.
    
    Args:
        video_path: Caminho para o arquivo de vídeo.
        method: Método de detecção ('adaptive' ou 'content').
        adaptive_threshold: Threshold para AdaptiveDetector.
        content_threshold: Threshold para ContentDetector.
    
    Returns:
        Informações da detecção de cenas.
    """
    
    try:
        self.update_state(
            state='PROGRESS',
            meta={'current': 0, 'total': 100, 'status': 'Iniciando detecção de cenas...'}
        )
        
        detector = SceneDetector(
            adaptive_threshold=adaptive_threshold,
            content_threshold=content_threshold
        )
        
        scene_list = detector.detect_scenes(video_path, method)
        
        # Converter FrameTimecode para um formato serializável (string de tempo e frame number)
        scenes_json = [
            {
                'start_time': str(scene[0].get_seconds()),
                'end_time': str(scene[1].get_seconds()),
                'start_frame': scene[0].frame_num,
                'end_frame': scene[1].frame_num,
                'duration': (scene[1] - scene[0]).get_seconds()
            }
            for scene in scene_list
        ]
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 100, 'total': 100, 'status': f'Detecção concluída! {len(scenes_json)} cenas encontradas.'}
        )
        
        logger.info(f"Detecção de cenas concluída: {len(scenes_json)} cenas.")
        return {
            'status': 'success',
            'scenes_count': len(scenes_json),
            'scenes': scenes_json,
            'video_path': video_path,
        }
    
    except Exception as exc:
        logger.error(f"Erro na detecção de cenas: {str(exc)}")
        # Não faremos retry para evitar reprocessamento de vídeo longo
        raise
