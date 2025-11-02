"""
Módulo de coleta de vídeos do YouTube com suporte a múltiplas chaves de API.
Responsável apenas pela lógica de busca e download usando yt-dlp.
Com fallback automático para outras chaves em caso de falha.
"""

import logging
from typing import List, Optional
import yt_dlp
from datetime import datetime, timedelta
from src.modules.api_key_manager import YouTubeKeyManager
from src.settings import get_settings

logger = logging.getLogger(__name__)


class YouTubeCollectorWithFallback:
    """Classe responsável pela coleta de vídeos do YouTube com fallback de chaves."""
    
    def __init__(self, channel_ids: dict):
        """
        Inicializa o coletor com gerenciador de chaves.
        
        Args:
            channel_ids: Dicionário com IDs dos canais
        """
        self.channel_ids = channel_ids
        self.ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': 'in_playlist',
            'skip_download': True,
        }
        
        # Inicializar gerenciador de chaves YouTube
        settings = get_settings()
        youtube_keys = settings.get_youtube_keys()
        self.key_manager = YouTubeKeyManager(youtube_keys)
        
        if youtube_keys:
            logger.info(f"YouTube Collector inicializado com {len(youtube_keys)} chave(s)")
        else:
            logger.warning("Nenhuma chave YouTube fornecida")
    
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
        Com retry automático em caso de falha de chave.
        
        Args:
            search_query: Termo de busca
            channel_ids: Lista de IDs de canais para filtrar
            filter_by: Filtro por 'relevance' ou 'date'
            time_range: Intervalo de tempo
            max_duration: Duração máxima em minutos
        
        Returns:
            Lista de vídeos encontrados
        """
        logger.info(f"Iniciando busca manual: {search_query}")
        
        def _search_with_key(api_key: str) -> List[dict]:
            """Função interna que executa a busca com uma chave específica."""
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
        
        # Tentar com fallback de chaves
        try:
            return self.key_manager.retry_with_fallback(
                _search_with_key,
                max_retries=3,
                delay=2.0
            )
        except Exception as e:
            logger.error(f"Falha na busca manual após todas as chaves: {str(e)}")
            raise
    
    def search_auto(self) -> List[dict]:
        """
        Busca automaticamente "Jogo Completo" e "Melhores Momentos".
        Com retry automático em caso de falha de chave.
        
        Returns:
            Lista de vídeos encontrados
        """
        logger.info("Iniciando busca automática")
        
        def _search_with_key(api_key: str) -> List[dict]:
            """Função interna que executa a busca automática com uma chave."""
            videos = []
            queries = ["Jogo Completo", "Melhores Momentos"]
            
            try:
                for query in queries:
                    logger.info(f"Buscando: {query}")
                    search_url = f"https://www.youtube.com/results?search_query={query}"
                    
                    with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                        info = ydl.extract_info(search_url, download=False)
                        
                        if info and 'entries' in info:
                            for entry in info['entries'][:10]:
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
        
        # Tentar com fallback de chaves
        try:
            return self.key_manager.retry_with_fallback(
                _search_with_key,
                max_retries=3,
                delay=2.0
            )
        except Exception as e:
            logger.error(f"Falha na busca automática após todas as chaves: {str(e)}")
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
    
    def get_key_status(self) -> dict:
        """Retorna o status do gerenciador de chaves."""
        return {
            'total_keys': len(self.key_manager.api_keys),
            'current_key_index': self.key_manager.current_key_index,
            'failed_keys_count': len(self.key_manager.failed_keys),
            'available_keys': len(self.key_manager.api_keys) - self.key_manager.current_key_index
        }
