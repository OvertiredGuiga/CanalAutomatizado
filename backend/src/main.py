"""
Aplicação FastAPI principal.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.settings import get_settings
from src.api.collect import router as collect_router
from src.api.download import router as download_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obter configurações
settings = get_settings()

# Criar aplicação FastAPI
app = FastAPI(
    title="Flamengo AI Creator - Coleta de Vídeos",
    description="API para coleta automatizada de vídeos do YouTube",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(collect_router)
app.include_router(download_router)


@app.get("/")
async def root():
    """Endpoint raiz da API."""
    return {
        "message": "Bem-vindo à API de Coleta de Vídeos do Flamengo AI Creator",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da aplicação."""
    return {
        "status": "healthy",
        "service": "Flamengo AI Creator - Coleta de Vídeos",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=settings.fastapi_debug,
    )
