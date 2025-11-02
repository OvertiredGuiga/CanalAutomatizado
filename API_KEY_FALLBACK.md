# Sistema de Fallback de Chaves de API

## Visão Geral

O projeto agora suporta **múltiplas chaves de API com fallback automático**. Se uma chave falhar ou atingir o limite de requisições, o sistema tenta automaticamente a próxima chave disponível.

## Chaves Suportadas

### OpenAI (até 4 chaves)
```env
OPENAI_API_KEY=sk-proj-...
OPENAI_API_KEY_2=sk-proj-...
OPENAI_API_KEY_3=sk-proj-...
OPENAI_API_KEY_4=sk-proj-...
```

### YouTube Data API (até 4 chaves)
```env
YOUTUBE_API_KEY=AIzaSy...
YOUTUBE_API_KEY_2=AIzaSy...
YOUTUBE_API_KEY_3=AIzaSy...
YOUTUBE_API_KEY_4=AIzaSy...
```

### RapidAPI
```env
RAPIDAPI_KEY=...
```

## Como Funciona

### 1. Inicialização

Quando a aplicação inicia, o `APIKeyManager` carrega todas as chaves disponíveis:

```python
from src.modules.api_key_manager import OpenAIKeyManager
from src.settings import get_settings

settings = get_settings()
openai_keys = settings.get_openai_keys()  # Retorna lista de chaves válidas
key_manager = OpenAIKeyManager(openai_keys)
```

### 2. Tentativa de Requisição

O sistema tenta usar a primeira chave:

```python
result = key_manager.retry_with_fallback(
    func=minha_funcao_api,
    max_retries=3,      # 3 tentativas por chave
    delay=1.0           # 1 segundo entre tentativas
)
```

### 3. Fallback Automático

Se a chave falhar:
1. Tenta novamente até `max_retries` vezes (com delay entre tentativas)
2. Se todas as tentativas falharem, marca a chave como falha
3. Passa para a próxima chave disponível
4. Repete o processo até ter sucesso ou esgotar todas as chaves

### 4. Logging

Cada tentativa é registrada:

```
INFO: OpenAI: Usando chave 1/4
WARNING: OpenAI: Erro na tentativa 1/3: Rate limit exceeded
INFO: OpenAI: Tentativa 2/3 com chave 1/4
WARNING: OpenAI: Erro na tentativa 2/3: Rate limit exceeded
INFO: OpenAI: Tentativa 3/3 com chave 1/4
WARNING: OpenAI: Chave 1/4 falhou. Tentando próxima chave...
INFO: OpenAI: Usando chave 2/4
INFO: OpenAI: Tentativa 1/3 com chave 2/4
INFO: OpenAI: Sucesso com chave 2/4
```

## Implementação

### Módulo: `api_key_manager.py`

Contém as classes principais:

- **`APIKeyManager`**: Classe base para gerenciar múltiplas chaves
- **`OpenAIKeyManager`**: Especializada para chaves OpenAI
- **`YouTubeKeyManager`**: Especializada para chaves YouTube
- **`retry_with_api_key_fallback`**: Decorator para aplicar fallback

### Exemplo de Uso

```python
from src.modules.api_key_manager import OpenAIKeyManager
from src.settings import get_settings

# Inicializar gerenciador
settings = get_settings()
openai_keys = settings.get_openai_keys()
key_manager = OpenAIKeyManager(openai_keys)

# Função que usa a API
def chamar_openai(api_key: str, prompt: str):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response

# Executar com fallback automático
try:
    resultado = key_manager.retry_with_fallback(
        func=chamar_openai,
        prompt="Olá, como você está?",
        max_retries=3,
        delay=2.0
    )
    print(resultado)
except Exception as e:
    print(f"Falha após todas as chaves: {e}")
```

## Configuração do .env

Adicione suas chaves no arquivo `.env`:

```env
# OpenAI
OPENAI_API_KEY=sk-proj-sua-chave-1
OPENAI_API_KEY_2=sk-proj-sua-chave-2
OPENAI_API_KEY_3=sk-proj-sua-chave-3
OPENAI_API_KEY_4=sk-proj-sua-chave-4

# YouTube
YOUTUBE_API_KEY=AIzaSy-sua-chave-1
YOUTUBE_API_KEY_2=AIzaSy-sua-chave-2
YOUTUBE_API_KEY_3=AIzaSy-sua-chave-3
YOUTUBE_API_KEY_4=AIzaSy-sua-chave-4

# RapidAPI
RAPIDAPI_KEY=sua-chave-rapidapi
```

**Nota:** Você pode deixar algumas chaves vazias. O sistema automaticamente filtra chaves vazias.

## Métodos Disponíveis

### `APIKeyManager`

```python
# Obter chave atual
chave = key_manager.get_current_key()

# Marcar chave como falha e ir para próxima
sucesso = key_manager.mark_key_failed()

# Resetar gerenciador
key_manager.reset()

# Obter todas as chaves
todas_chaves = key_manager.get_all_keys()

# Obter chaves que falharam
chaves_falhadas = key_manager.get_failed_keys()

# Executar com retry e fallback
resultado = key_manager.retry_with_fallback(
    func=minha_funcao,
    arg1=valor1,
    max_retries=3,
    delay=1.0
)
```

## Monitoramento e Debugging

### Ver Status das Chaves

```python
# Status atual
status = key_manager.get_current_key()
print(f"Chave atual: {status}")

# Chaves falhadas
falhadas = key_manager.get_failed_keys()
print(f"Chaves falhadas: {len(falhadas)}")

# Índice atual
print(f"Índice: {key_manager.current_key_index}")
```

### Logs

O sistema registra automaticamente:
- Qual chave está sendo usada
- Tentativas de requisição
- Erros e falhas
- Mudança para próxima chave
- Sucesso ou falha final

Verifique os logs para entender o fluxo:

```bash
# No terminal do Celery ou FastAPI
# Procure por mensagens como:
# INFO: OpenAI: Usando chave 1/4
# WARNING: OpenAI: Chave 1/4 falhou. Tentando próxima chave...
```

## Casos de Uso

### 1. Rate Limiting

Se uma chave atinge o limite de requisições:
```
OpenAI: Erro: Rate limit exceeded
OpenAI: Chave 1/4 falhou. Tentando próxima chave...
OpenAI: Usando chave 2/4
```

### 2. Chave Inválida

Se uma chave é inválida ou expirada:
```
OpenAI: Erro: Invalid API key
OpenAI: Chave 1/4 falhou. Tentando próxima chave...
```

### 3. Falha de Rede

Se há problema de conectividade:
```
OpenAI: Erro: Connection timeout
OpenAI: Tentativa 2/3 com chave 1/4
OpenAI: Erro: Connection timeout
OpenAI: Tentativa 3/3 com chave 1/4
OpenAI: Chave 1/4 falhou. Tentando próxima chave...
```

## Boas Práticas

1. **Múltiplas Chaves:** Sempre mantenha pelo menos 2 chaves para cada API
2. **Monitoramento:** Verifique os logs regularmente para identificar chaves problemáticas
3. **Rotação:** Considere rotacionar chaves periodicamente
4. **Limites:** Distribua o uso entre chaves para evitar atingir limites
5. **Segurança:** Nunca commite chaves reais no repositório (use `.env`)

## Próximas Melhorias

- [ ] Persistência de estado de chaves (qual chave falhou)
- [ ] Métricas de uso por chave
- [ ] Dashboard de monitoramento
- [ ] Alertas automáticos quando chaves falham
- [ ] Suporte a WebSocket para atualização em tempo real
