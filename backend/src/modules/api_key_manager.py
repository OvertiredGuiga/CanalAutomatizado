"""
Gerenciador de chaves de API com fallback automático.
Tenta usar uma chave de API e, em caso de falha, tenta a próxima.
"""

import logging
from typing import List, Optional, Callable, Any
from functools import wraps
import time

logger = logging.getLogger(__name__)


class APIKeyManager:
    """
    Gerenciador de múltiplas chaves de API com suporte a fallback automático.
    """
    
    def __init__(self, api_keys: List[str], api_name: str = "API"):
        """
        Inicializa o gerenciador de chaves.
        
        Args:
            api_keys: Lista de chaves de API
            api_name: Nome da API para logging
        """
        self.api_keys = [key for key in api_keys if key]  # Filtrar chaves vazias
        self.api_name = api_name
        self.current_key_index = 0
        self.failed_keys = set()
        
        if not self.api_keys:
            logger.warning(f"Nenhuma chave de API válida fornecida para {api_name}")
    
    def get_current_key(self) -> Optional[str]:
        """Retorna a chave de API atual."""
        if self.current_key_index < len(self.api_keys):
            return self.api_keys[self.current_key_index]
        return None
    
    def mark_key_failed(self) -> bool:
        """
        Marca a chave atual como falha e tenta a próxima.
        
        Returns:
            True se há uma próxima chave disponível, False caso contrário
        """
        current_key = self.get_current_key()
        if current_key:
            self.failed_keys.add(current_key)
            logger.warning(
                f"{self.api_name}: Chave {self.current_key_index + 1}/{len(self.api_keys)} falhou. "
                f"Tentando próxima chave..."
            )
        
        # Tentar próxima chave
        self.current_key_index += 1
        
        if self.current_key_index < len(self.api_keys):
            logger.info(
                f"{self.api_name}: Usando chave {self.current_key_index + 1}/{len(self.api_keys)}"
            )
            return True
        else:
            logger.error(
                f"{self.api_name}: Todas as {len(self.api_keys)} chaves falharam!"
            )
            return False
    
    def reset(self) -> None:
        """Reseta o gerenciador para a primeira chave."""
        self.current_key_index = 0
        self.failed_keys.clear()
        logger.info(f"{self.api_name}: Gerenciador resetado para a primeira chave")
    
    def get_all_keys(self) -> List[str]:
        """Retorna todas as chaves disponíveis."""
        return self.api_keys.copy()
    
    def get_failed_keys(self) -> set:
        """Retorna o conjunto de chaves que falharam."""
        return self.failed_keys.copy()
    
    def retry_with_fallback(
        self,
        func: Callable,
        *args,
        max_retries: int = 3,
        delay: float = 1.0,
        **kwargs
    ) -> Any:
        """
        Executa uma função com retry automático usando fallback de chaves.
        
        Args:
            func: Função a executar
            max_retries: Número máximo de tentativas por chave
            delay: Delay em segundos entre tentativas
            *args: Argumentos posicionais para a função
            **kwargs: Argumentos nomeados para a função
        
        Returns:
            Resultado da função se bem-sucedida
        
        Raises:
            Exception: Se todas as chaves falharem
        """
        last_error = None
        
        while self.current_key_index < len(self.api_keys):
            current_key = self.get_current_key()
            
            for attempt in range(max_retries):
                try:
                    logger.info(
                        f"{self.api_name}: Tentativa {attempt + 1}/{max_retries} "
                        f"com chave {self.current_key_index + 1}/{len(self.api_keys)}"
                    )
                    
                    # Passar a chave atual como argumento
                    result = func(current_key, *args, **kwargs)
                    
                    logger.info(
                        f"{self.api_name}: Sucesso com chave {self.current_key_index + 1}"
                    )
                    return result
                
                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"{self.api_name}: Erro na tentativa {attempt + 1}/{max_retries}: {str(e)}"
                    )
                    
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            
            # Se chegou aqui, todas as tentativas falharam com esta chave
            if not self.mark_key_failed():
                break
        
        # Se chegou aqui, todas as chaves falharam
        error_msg = (
            f"{self.api_name}: Falha após tentar todas as "
            f"{len(self.api_keys)} chaves. Último erro: {str(last_error)}"
        )
        logger.error(error_msg)
        raise Exception(error_msg)


class OpenAIKeyManager(APIKeyManager):
    """Gerenciador específico para chaves OpenAI."""
    
    def __init__(self, api_keys: List[str]):
        super().__init__(api_keys, api_name="OpenAI")


class YouTubeKeyManager(APIKeyManager):
    """Gerenciador específico para chaves YouTube."""
    
    def __init__(self, api_keys: List[str]):
        super().__init__(api_keys, api_name="YouTube")


def retry_with_api_key_fallback(
    api_key_manager: APIKeyManager,
    max_retries: int = 3,
    delay: float = 1.0
):
    """
    Decorator para aplicar retry com fallback de chaves de API.
    
    Args:
        api_key_manager: Instância do APIKeyManager
        max_retries: Número máximo de tentativas por chave
        delay: Delay em segundos entre tentativas
    
    Returns:
        Função decorada
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return api_key_manager.retry_with_fallback(
                func,
                *args,
                max_retries=max_retries,
                delay=delay,
                **kwargs
            )
        return wrapper
    return decorator
