"""
Módulo de coleta de vídeos do YouTube.
Responsável apenas pela lógica de busca e download usando yt-dlp.
"""

import logging
from typing import List, Optional
import yt_dlp
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class YouTubeCollector:
    """Classe responsável pela coleta de vídeos do YouTube."""
    
    def __init__(self, channel_ids: dict):
        """
        Inicializa o coletor.
        
        Args:
            channel_ids: Dicionário com IDs dos canais (ex: {'getv': 'UCxxx', 'cazetv': 'UCyyy'})
        """
        self.channel_ids = channel_ids
        self.ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': 'in_playlist',
            'skip_download': True,
        }
    
    def search_manual(
        self,
        search_query: str,
        channel_ids: Optional[List[str]] = None,
        filter_by: str = "relevance",
        time_range: str = "any",
        max_duration: Optional[int] = None,
    ) -> List[dict]:
        """
        Busca vídeos manualmente usando uma query de pesquisa.
        
        Args:
            search_query: Termo de busca
            channel_ids: Lista de IDs de canais para filtrar
            filter_by: Filtro por 'relevance' ou 'date'
            time_range: Intervalo de tempo ('any', 'hour', 'day', 'week', 'month', 'year')
            max_duration: Duração máxima em minutos (opcional)
        
        Returns:
            Lista de vídeos encontrados
        """
        logger.info(f"Iniciando busca manual: {search_query}")
        
        videos = []
        
        try:
            # Construir a URL de busca do YouTube
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(search_url, download=False)
                
                if info and 'entries' in info:
                    for entry in info['entries'][:20]:  # Limitar a 20 resultados
                        video_info = {
                            'video_id': entry.get('id'),
                            'title': entry.get('title'),
                            'channel': entry.get('uploader'),
                            'duration': entry.get('duration'),
                            'upload_date': entry.get('upload_date'),
                            'url': f"https://www.youtube.com/watch?v={entry.get('id')}"
                        }
                        
                        # Filtrar por duração se especificado
                        if max_duration and entry.get('duration'):
                            if entry.get('duration') > max_duration * 60:
                                continue
                        
                        videos.append(video_info)
            
            logger.info(f"Encontrados {len(videos)} vídeos na busca manual")
            return videos
        
        except Exception as e:
            logger.error(f"Erro na busca manual: {str(e)}")
            raise
    
    def search_auto(self) -> List[dict]:
        """
        Busca automaticamente "Jogo Completo" e "Melhores Momentos" dos canais GETV e CazeTV.
        
        Returns:
            Lista de vídeos encontrados
        """
        logger.info("Iniciando busca automática")
        
        videos = []
        queries = ["Jogo Completo", "Melhores Momentos"]
        
        try:
            for query in queries:
                logger.info(f"Buscando: {query}")
                search_url = f"https://www.youtube.com/results?search_query={query}"
                
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    info = ydl.extract_info(search_url, download=False)
                    
                    if info and 'entries' in info:
                        for entry in info['entries'][:10]:  # Limitar a 10 resultados por query
                            # Filtrar por data recente (últimos 7 dias)
                            upload_date = entry.get('upload_date')
                            if upload_date:
                                try:
                                    date_obj = datetime.strptime(upload_date, '%Y%m%d')
                                    if datetime.now() - date_obj > timedelta(days=7):
                                        continue
                                except ValueError:
                                    pass
                            
                            video_info = {
                                'video_id': entry.get('id'),
                                'title': entry.get('title'),
                                'channel': entry.get('uploader'),
                                'duration': entry.get('duration'),
                                'upload_date': entry.get('upload_date'),
                                'url': f"https://www.youtube.com/watch?v={entry.get('id')}"
                            }
                            videos.append(video_info)
            
            logger.info(f"Encontrados {len(videos)} vídeos na busca automática")
            return videos
        
        except Exception as e:
            logger.error(f"Erro na busca automática: {str(e)}")
            raise
    
    def download_video(self, video_url: str, output_path: str = "downloads") -> dict:
        """
        Faz o download de um vídeo do YouTube.
        
        Args:
            video_url: URL do vídeo
            output_path: Caminho para salvar o vídeo
        
        Returns:
            Informações do vídeo baixado
        """
        logger.info(f"Iniciando download: {video_url}")
        
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                
                download_info = {
                    'video_id': info.get('id'),
                    'title': info.get('title'),
                    'filename': ydl.prepare_filename(info),
                    'duration': info.get('duration'),
                    'url': video_url,
                    'status': 'downloaded'
                }
                
                logger.info(f"Download concluído: {info.get('title')}")
                return download_info
        
        except Exception as e:
            logger.error(f"Erro no download: {str(e)}")
            raise
