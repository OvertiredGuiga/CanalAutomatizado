"""
Rotas da API para coleta de vídeos.
Responsável apenas pela validação da requisição e disparo da tarefa Celery.
"""

import logging
from fastapi import APIRouter, HTTPException
from src.models import CollectRequest, CollectResponse, TaskStatusResponse
from src.tasks import collect_youtube_videos

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/collect", tags=["collect"])


@router.post("/youtube", response_model=CollectResponse)
async def collect_youtube(request: CollectRequest) -> CollectResponse:
    """
    Dispara uma tarefa de coleta de vídeos do YouTube.
    
    Args:
        request: Requisição com parâmetros de coleta
    
    Returns:
        Resposta com ID da tarefa e status
    
    Raises:
        HTTPException: Se houver erro ao disparar a tarefa
    """
    
    try:
        logger.info(f"Disparando tarefa de coleta: {request.mode}")
        
        # Disparar tarefa Celery de forma não-bloqueante
        task = collect_youtube_videos.delay(
            mode=request.mode.value,
            search_query=request.search_query or "",
            channel_ids=request.channel_ids or [],
            filter_by=request.filter_by.value,
            time_range=request.time_range.value,
            max_duration=request.max_duration,
        )
        
        logger.info(f"Tarefa disparada com ID: {task.id}")
        
        return CollectResponse(
            task_id=task.id,
            status="PENDING",
            message="Tarefa de coleta iniciada com sucesso",
        )
    
    except Exception as e:
        logger.error(f"Erro ao disparar tarefa: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao iniciar coleta: {str(e)}"
        )


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """
    Retorna o status de uma tarefa Celery.
    
    Args:
        task_id: ID da tarefa
    
    Returns:
        Status atual da tarefa
    
    Raises:
        HTTPException: Se a tarefa não for encontrada
    """
    
    try:
        logger.info(f"Consultando status da tarefa: {task_id}")
        
        task = collect_youtube_videos.AsyncResult(task_id)
        
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
                progress=task.info.get('progress', {}) if isinstance(task.info, dict) else task.info
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
        
        logger.info(f"Status da tarefa {task_id}: {task.state}")
        return response
    
    except Exception as e:
        logger.error(f"Erro ao consultar status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar status: {str(e)}"
        )
