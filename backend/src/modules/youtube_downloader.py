"""
Módulo para download de vídeos do YouTube usando yt-dlp.
Responsável apenas pela lógica de download.
"""

import logging
import os
from pathlib import Path
from typing import Optional, Callable
import yt_dlp

logger = logging.getLogger(__name__)


class YouTubeDownloader:
    """Classe responsável pelo download de vídeos do YouTube."""
    
    def __init__(self, output_path: str = "downloads"):
        """
        Inicializa o downloader.
        
        Args:
            output_path: Caminho para salvar os vídeos
        """
        self.output_path = output_path
        
        # Criar diretório se não existir
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"YouTubeDownloader inicializado com output: {output_path}")
    
    def download_video(
        self,
        video_url: str,
        format_choice: str = "best",
        progress_callback: Optional[Callable] = None,
    ) -> dict:
        """
        Faz o download de um vídeo do YouTube.
        
        Args:
            video_url: URL do vídeo
            format_choice: Formato desejado ('best', 'best[ext=mp4]', etc)
            progress_callback: Callback para atualizar progresso
        
        Returns:
            Dicionário com informações do download
        
        Raises:
            Exception: Se houver erro no download
        """
        logger.info(f"Iniciando download: {video_url}")
        
        # Configurar opções do yt-dlp
        ydl_opts = {
            'format': format_choice,
            'outtmpl': os.path.join(self.output_path, '%(id)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook] if progress_callback else [],
        }
        
        # Armazenar callback para uso no hook
        self._progress_callback = progress_callback
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Extraindo informações do vídeo...")
                info = ydl.extract_info(video_url, download=True)
                
                filename = ydl.prepare_filename(info)
                file_size = os.path.getsize(filename) if os.path.exists(filename) else 0
                
                download_info = {
                    'status': 'success',
                    'video_id': info.get('id'),
                    'title': info.get('title'),
                    'filename': filename,
                    'file_size': file_size,
                    'duration': info.get('duration'),
                    'url': video_url,
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date'),
                }
                
                logger.info(f"Download concluído: {info.get('title')}")
                return download_info
        
        except Exception as e:
            logger.error(f"Erro no download: {str(e)}")
            raise
    
    def _progress_hook(self, d: dict) -> None:
        """
        Hook para atualizar progresso do download.
        
        Args:
            d: Dicionário com informações do progresso
        """
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            
            progress_info = {
                'status': 'downloading',
                'percent': percent,
                'speed': speed,
                'eta': eta,
                'total_bytes': d.get('total_bytes', 0),
                'downloaded_bytes': d.get('downloaded_bytes', 0),
            }
            
            if self._progress_callback:
                self._progress_callback(progress_info)
        
        elif d['status'] == 'finished':
            logger.info("Download finalizado, processando arquivo...")
            if self._progress_callback:
                self._progress_callback({'status': 'finished'})
    
    def download_multiple_videos(
        self,
        video_urls: list,
        format_choice: str = "best",
        progress_callback: Optional[Callable] = None,
    ) -> dict:
        """
        Faz o download de múltiplos vídeos.
        
        Args:
            video_urls: Lista de URLs
            format_choice: Formato desejado
            progress_callback: Callback para progresso
        
        Returns:
            Dicionário com resultados
        """
        logger.info(f"Iniciando download de {len(video_urls)} vídeos")
        
        results = {
            'total': len(video_urls),
            'successful': 0,
            'failed': 0,
            'videos': [],
            'errors': [],
        }
        
        for idx, url in enumerate(video_urls):
            try:
                if progress_callback:
                    progress_callback({
                        'status': 'downloading_multiple',
                        'current': idx + 1,
                        'total': len(video_urls),
                        'url': url,
                    })
                
                video_info = self.download_video(url, format_choice)
                results['videos'].append(video_info)
                results['successful'] += 1
            
            except Exception as e:
                logger.error(f"Erro ao baixar {url}: {str(e)}")
                results['errors'].append({
                    'url': url,
                    'error': str(e),
                })
                results['failed'] += 1
        
        logger.info(
            f"Download múltiplo concluído: "
            f"{results['successful']} sucesso, {results['failed']} falhas"
        )
        
        return results
    
    def get_video_info(self, video_url: str) -> dict:
        """
        Obtém informações de um vídeo sem fazer download.
        
        Args:
            video_url: URL do vídeo
        
        Returns:
            Dicionário com informações do vídeo
        """
        logger.info(f"Obtendo informações: {video_url}")
        
        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'skip_download': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                video_info = {
                    'video_id': info.get('id'),
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description'),
                    'thumbnail': info.get('thumbnail'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'formats_available': len(info.get('formats', [])),
                }
                
                logger.info(f"Informações obtidas: {info.get('title')}")
                return video_info
        
        except Exception as e:
            logger.error(f"Erro ao obter informações: {str(e)}")
            raise
    
    def get_available_formats(self, video_url: str) -> list:
        """
        Retorna formatos disponíveis para download.
        
        Args:
            video_url: URL do vídeo
        
        Returns:
            Lista de formatos disponíveis
        """
        logger.info(f"Obtendo formatos disponíveis: {video_url}")
        
        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'skip_download': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                formats = []
                for fmt in info.get('formats', []):
                    format_info = {
                        'format_id': fmt.get('format_id'),
                        'format': fmt.get('format'),
                        'ext': fmt.get('ext'),
                        'resolution': fmt.get('resolution', 'N/A'),
                        'fps': fmt.get('fps'),
                        'vcodec': fmt.get('vcodec'),
                        'acodec': fmt.get('acodec'),
                        'filesize': fmt.get('filesize'),
                    }
                    formats.append(format_info)
                
                logger.info(f"Encontrados {len(formats)} formatos")
                return formats
        
        except Exception as e:
            logger.error(f"Erro ao obter formatos: {str(e)}")
            raise
