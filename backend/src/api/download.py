"""
Rotas da API para download de vídeos.
Responsável apenas pela validação da requisição e disparo da tarefa Celery.
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.tasks_download import download_youtube_video, download_multiple_youtube_videos, get_video_info_task, get_available_formats_task
from src.models import TaskStatusResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/download", tags=["download"])


class DownloadRequest(BaseModel):
    """Requisição para download de vídeo."""
    video_url: str
    format_choice: str = "best"


class DownloadResponse(BaseModel):
    """Resposta de download."""
    task_id: str
    status: str
    message: str


class MultipleDownloadRequest(BaseModel):
    """Requisição para download múltiplo."""
    video_urls: list[str]
    format_choice: str = "best"


class VideoInfoRequest(BaseModel):
    """Requisição para obter informações do vídeo."""
    video_url: str


@router.post("/video", response_model=DownloadResponse)
async def download_video(request: DownloadRequest) -> DownloadResponse:
    """
    Dispara uma tarefa de download de um vídeo do YouTube.
    
    Args:
        request: Requisição com URL do vídeo
    
    Returns:
        Resposta com ID da tarefa e status
    
    Raises:
        HTTPException: Se houver erro ao disparar a tarefa
    """
    
    try:
        if not request.video_url:
            raise ValueError("URL do vídeo é obrigatória")
        
        logger.info(f"Disparando tarefa de download: {request.video_url}")
        
        # Disparar tarefa Celery de forma não-bloqueante
        task = download_youtube_video.delay(
            video_url=request.video_url,
            format_choice=request.format_choice,
        )
        
        logger.info(f"Tarefa de download disparada com ID: {task.id}")
        
        return DownloadResponse(
            task_id=task.id,
            status="PENDING",
            message="Tarefa de download iniciada com sucesso",
        )
    
    except Exception as e:
        logger.error(f"Erro ao disparar tarefa de download: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao iniciar download: {str(e)}"
        )


@router.post("/multiple", response_model=DownloadResponse)
async def download_multiple_videos(request: MultipleDownloadRequest) -> DownloadResponse:
    """
    Dispara uma tarefa de download de múltiplos vídeos.
    
    Args:
        request: Requisição com lista de URLs
    
    Returns:
        Resposta com ID da tarefa e status
    
    Raises:
        HTTPException: Se houver erro ao disparar a tarefa
    """
    
    try:
        if not request.video_urls or len(request.video_urls) == 0:
            raise ValueError("Lista de URLs é obrigatória")
        
        logger.info(f"Disparando tarefa de download múltiplo: {len(request.video_urls)} vídeos")
        
        # Disparar tarefa Celery de forma não-bloqueante
        task = download_multiple_youtube_videos.delay(
            video_urls=request.video_urls,
            format_choice=request.format_choice,
        )
        
        logger.info(f"Tarefa de download múltiplo disparada com ID: {task.id}")
        
        return DownloadResponse(
            task_id=task.id,
            status="PENDING",
            message=f"Tarefa de download de {len(request.video_urls)} vídeos iniciada com sucesso",
        )
    
    except Exception as e:
        logger.error(f"Erro ao disparar tarefa de download múltiplo: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao iniciar downloads: {str(e)}"
        )


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_download_status(task_id: str) -> TaskStatusResponse:
    """
    Retorna o status de uma tarefa de download.
    
    Args:
        task_id: ID da tarefa
    
    Returns:
        Status atual da tarefa
    
    Raises:
        HTTPException: Se a tarefa não for encontrada
    """
    
    try:
        logger.info(f"Consultando status da tarefa de download: {task_id}")
        
        task = download_youtube_video.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = TaskStatusResponse(
                task_id=task_id,
                status='PENDING',
                progress={'current': 0, 'total': 100, 'status': 'Aguardando processamento...'}
            )
        elif task.state == 'PROGRESS':
            response = TaskStatusResponse(
                task_id=task_id,
                status='PROGRESS',
                progress=task.info if isinstance(task.info, dict) else {'status': str(task.info)}
            )
        elif task.state == 'SUCCESS':
            response = TaskStatusResponse(
                task_id=task_id,
                status='SUCCESS',
                result=task.result
            )
        elif task.state == 'FAILURE':
            response = TaskStatusResponse(
                task_id=task_id,
                status='FAILURE',
                error=str(task.info)
            )
        else:
            response = TaskStatusResponse(
                task_id=task_id,
                status=task.state,
                result=task.result if task.state == 'SUCCESS' else None
            )
        
        logger.info(f"Status da tarefa de download {task_id}: {task.state}")
        return response
    
    except Exception as e:
        logger.error(f"Erro ao consultar status do download: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar status: {str(e)}"
        )


@router.post("/video-info")
async def get_video_info(request: VideoInfoRequest):
    """
    Obtém informações de um vídeo sem fazer download.
    
    Args:
        request: Requisição com URL do vídeo
    
    Returns:
        Informações do vídeo
    
    Raises:
        HTTPException: Se houver erro
    """
    
    try:
        logger.info(f"Obtendo informações do vídeo: {request.video_url}")
        
        task = get_video_info_task.delay(video_url=request.video_url)
        
        return {
            'task_id': task.id,
            'status': 'PENDING',
            'message': 'Obtendo informações do vídeo...'
        }
    
    except Exception as e:
        logger.error(f"Erro ao obter informações: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter informações: {str(e)}"
        )


@router.post("/formats")
async def get_formats(request: VideoInfoRequest):
    """
    Obtém formatos disponíveis para download.
    
    Args:
        request: Requisição com URL do vídeo
    
    Returns:
        Lista de formatos disponíveis
    
    Raises:
        HTTPException: Se houver erro
    """
    
    try:
        logger.info(f"Obtendo formatos disponíveis: {request.video_url}")
        
        task = get_available_formats_task.delay(video_url=request.video_url)
        
        return {
            'task_id': task.id,
            'status': 'PENDING',
            'message': 'Obtendo formatos disponíveis...'
        }
    
    except Exception as e:
        logger.error(f"Erro ao obter formatos: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter formatos: {str(e)}"
        )
