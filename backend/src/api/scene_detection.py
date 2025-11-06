"""
Endpoints FastAPI para detecção de cenas.
"""

import logging
import os
import shutil
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from celery.result import AsyncResult
from src.tasks_scene_detection import detect_scenes_task

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scene-detection", tags=["scene-detection"])

# Diretório temporário para uploads de vídeo
TEMP_UPLOAD_DIR = "/tmp/video_uploads"
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

@router.post("/detect")
async def detect_scenes(
    file: UploadFile = File(..., description="Arquivo de vídeo para análise."),
    method: str = "adaptive",
    adaptive_threshold: float = 3.0,
    content_threshold: float = 27.0,
):
    """
    Inicia a detecção de cenas em um vídeo.
    O vídeo é salvo temporariamente e a tarefa é enfileirada no Celery.
    """
    
    # 1. Salvar arquivo temporário com nome padronizado (sem espaços)
    # Gerar um nome de arquivo seguro e único
    original_filename, file_extension = os.path.splitext(file.filename)
    # Remove espaços e caracteres especiais, mantendo apenas letras, números e hífens
    safe_filename = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in original_filename).strip('_')
    
    # Adicionar um timestamp ou UUID para garantir unicidade, mas por simplicidade, usaremos um nome seguro
    # Para o caso de upload, vamos usar um nome seguro e a extensão original
    
    # Se o nome seguro estiver vazio, use 'uploaded_file'
    if not safe_filename:
        safe_filename = "uploaded_file"
        
    # Construir o caminho final do arquivo
    file_location = os.path.join(TEMP_UPLOAD_DIR, f"{safe_filename}{file_extension}")
    
    # Se o arquivo já existir (improvável, mas possível), adicione um número
    counter = 1
    while os.path.exists(file_location):
        file_location = os.path.join(TEMP_UPLOAD_DIR, f"{safe_filename}_{counter}{file_extension}")
        counter += 1
        
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logger.info(f"Arquivo salvo temporariamente em: {file_location}")
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar o arquivo de vídeo.")
    finally:
        file.file.close()
    
    # 2. Enfileirar task no Celery
    task = detect_scenes_task.delay(
        video_path=file_location,
        method=method,
        adaptive_threshold=adaptive_threshold,
        content_threshold=content_threshold,
    )
    
    logger.info(f"Detecção de cenas iniciada. Task ID: {task.id}")
    
    return {
        'task_id': task.id,
        'status': 'processing',
        'message': 'Detecção de cenas iniciada. Use o endpoint /status/{task_id} para acompanhar.',
        'filename': file.filename,
    }

@router.get("/status/{task_id}")
async def get_scenes_status(task_id: str):
    """
    Obtém o status e o resultado da tarefa de detecção de cenas.
    """
    task = AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'status': task.state,
            'message': 'Tarefa pendente ou desconhecida.',
        }
    elif task.state == 'PROGRESS':
        response = {
            'task_id': task_id,
            'status': task.state,
            'progress': task.info.get('current', 0),
            'total': task.info.get('total', 100),
            'status_message': task.info.get('status', 'Processando...'),
        }
    elif task.state == 'SUCCESS':
        # O resultado contém a lista de cenas e o caminho do vídeo
        result = task.result
        
        # Limpar o arquivo temporário após o sucesso
        if 'video_path' in result and os.path.exists(result['video_path']):
            os.remove(result['video_path'])
            logger.info(f"Arquivo temporário removido: {result['video_path']}")
            # Remover o caminho do vídeo do resultado final para o frontend
            del result['video_path'] 
            
        response = {
            'task_id': task_id,
            'status': task.state,
            'result': result,
        }
    elif task.state == 'FAILURE':
        # Tentar obter a exceção
        error_message = str(task.info.get('error', 'Erro desconhecido durante o processamento.'))
        
        # Tentar limpar o arquivo temporário em caso de falha
        # O caminho do vídeo está nos args da task, que é um atributo privado, mas podemos tentar
        # O Celery armazena os args no backend, mas não é trivial acessar aqui.
        # Por simplicidade, vamos ignorar a limpeza em caso de falha por enquanto.
        
        response = {
            'task_id': task_id,
            'status': task.state,
            'error': error_message,
            'message': 'A tarefa falhou. Verifique os logs do Celery para mais detalhes.',
        }
    else:
        response = {
            'task_id': task_id,
            'status': task.state,
            'message': 'Status da tarefa desconhecido.',
        }
        
    return response
