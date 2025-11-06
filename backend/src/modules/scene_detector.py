"""
Módulo para detecção de cenas usando PySceneDetect.
"""

import logging
from scenedetect import detect, AdaptiveDetector, ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg
from scenedetect.frame_timecode import FrameTimecode

logger = logging.getLogger(__name__)

class SceneDetector:
    """
    Classe wrapper para o PySceneDetect.
    """
    def __init__(self, adaptive_threshold=3.0, content_threshold=27.0):
        self.adaptive_threshold = adaptive_threshold
        self.content_threshold = content_threshold
    
    def detect_scenes(self, video_path: str, method: str = 'adaptive') -> list[tuple[FrameTimecode, FrameTimecode]]:
        """
        Detecta cenas no vídeo usando o método especificado.
        
        Args:
            video_path: Caminho para o arquivo de vídeo.
            method: 'adaptive' ou 'content'.
            
        Returns:
            Lista de tuplas (start_timecode, end_timecode) representando as cenas.
        """
        logger.info(f"Iniciando detecção de cenas em {video_path} com método {method}")
        
        if method == 'adaptive':
            detector = AdaptiveDetector(
                adaptive_threshold=self.adaptive_threshold
            )
        elif method == 'content':
            detector = ContentDetector(
                threshold=self.content_threshold
            )
        else:
            raise ValueError(f"Método de detecção inválido: {method}. Use 'adaptive' ou 'content'.")
        
        try:
            scene_list = detect(video_path, detector)
            logger.info(f"Detecção concluída. {len(scene_list)} cenas encontradas.")
            return scene_list
        except Exception as e:
            logger.error(f"Erro durante a detecção de cenas: {e}")
            raise
    
    def split_video(self, video_path: str, scene_list: list[tuple[FrameTimecode, FrameTimecode]], output_dir: str = 'clips') -> None:
        """
        Divide o vídeo em clipes usando a lista de cenas detectadas.
        
        Args:
            video_path: Caminho para o arquivo de vídeo.
            scene_list: Lista de tuplas (start_timecode, end_timecode) representando as cenas.
            output_dir: Diretório para salvar os clipes.
        """
        logger.info(f"Iniciando divisão do vídeo {video_path} em {len(scene_list)} clipes no diretório {output_dir}")
        try:
            split_video_ffmpeg(video_path, scene_list, output_dir=output_dir)
            logger.info("Divisão do vídeo concluída.")
        except Exception as e:
            logger.error(f"Erro durante a divisão do vídeo: {e}")
            raise
