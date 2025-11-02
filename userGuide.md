# Guia de Usuário - Flamengo AI Creator

## Visão Geral

O **Flamengo AI Creator** é uma aplicação web para coleta automatizada de vídeos do YouTube. A aplicação é dividida em dois componentes principais: um backend robusto (FastAPI + Celery + Redis) e um frontend reativo (React + Vite).

## Inicialização dos Componentes

Para que a aplicação funcione corretamente, é necessário iniciar os 4 componentes na seguinte ordem:

### 1. Redis (Broker de Mensagens)

O Redis é usado como broker para o Celery e como backend de resultados.

```bash
# Instalar Redis (se não estiver instalado)
sudo apt-get install redis-server

# Iniciar o Redis
redis-server
```

**Porta padrão:** `6379`

### 2. Celery Worker (Processador de Tarefas)

O Celery processa as tarefas de coleta de forma assíncrona.

```bash
cd backend
source venv/bin/activate
celery -A src.celery_app worker --loglevel=info
```

**Saída esperada:** Mensagem indicando que o worker está pronto para receber tarefas.

### 3. FastAPI Backend (Servidor da API)

O FastAPI fornece os endpoints da API para coleta de vídeos.

```bash
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Porta padrão:** `8000`
**Documentação da API:** `http://localhost:8000/docs`

### 4. Vite Frontend (Aplicação Web)

O Vite fornece a interface web para interagir com a API.

```bash
cd frontend
npm run dev
```

**Porta padrão:** `5173`
**URL da aplicação:** `http://localhost:5173`

## Variáveis de Ambiente

### Backend (.env)

O arquivo `.env` no diretório `backend/` deve conter as seguintes configurações:

```env
# FastAPI Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_DEBUG=True

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# YouTube Channels
GETV_CHANNEL_ID=UCXXXXXXXXXXXXXXXXXXXXXXXx
CAZETV_CHANNEL_ID=UCYYYYYYYYYYYYYYYYYYYYYYYy

# OpenAI Configuration (optional)
OPENAI_API_KEY=sk-your-api-key-here
```

## Usando a Aplicação

### 1. Acessar a Interface Web

Abra seu navegador e acesse: `http://localhost:5173`

### 2. Formulário de Coleta

A aplicação apresenta um formulário com os seguintes campos:

**Modo de Coleta:**
- **Manual:** Permite especificar uma query de busca personalizada
- **Automático:** Busca automaticamente "Jogo Completo" e "Melhores Momentos" dos canais pré-configurados

**Campos do Modo Manual:**
- **Query de Busca:** Termo para buscar vídeos (ex: "Flamengo", "Jogo Completo")
- **Canais:** Selecione os canais desejados (GETV, CazeTV)
- **Filtrar por:** Relevância ou Data
- **Intervalo de Tempo:** Qualquer tempo, Última hora, Último dia, Última semana, Último mês, Último ano
- **Duração Máxima:** Limite de duração em minutos (opcional)

### 3. Iniciar a Coleta

Clique no botão **"Iniciar Coleta"** para disparar a tarefa. O botão mudará para **"Processando..."** enquanto a tarefa é executada.

### 4. Painel de Status

Após disparar a coleta, um painel de status aparecerá mostrando:

- **ID da Tarefa:** Identificador único da tarefa Celery
- **Status:** Estado atual da tarefa (Aguardando, Processando, Concluído, Falhou)
- **Progresso:** Barra de progresso com porcentagem e mensagem descritiva
- **Resultado:** Lista dos vídeos encontrados (quando concluído)
- **Erro:** Mensagem de erro (se houver falha)

## Endpoints da API

### POST /api/v1/collect/youtube

Dispara uma tarefa de coleta de vídeos.

**Request:**
```json
{
  "mode": "manual",
  "search_query": "Flamengo",
  "channel_ids": ["getv", "cazetv"],
  "filter_by": "date",
  "time_range": "week",
  "max_duration": 120
}
```

**Response:**
```json
{
  "task_id": "abc123def456",
  "status": "PENDING",
  "message": "Tarefa de coleta iniciada com sucesso"
}
```

### GET /api/v1/collect/status/{task_id}

Retorna o status de uma tarefa Celery.

**Response:**
```json
{
  "task_id": "abc123def456",
  "status": "PROGRESS",
  "progress": {
    "current": 50,
    "total": 100,
    "status": "Buscando vídeos..."
  },
  "result": null,
  "error": null
}
```

## Arquitetura

### Backend

- **FastAPI:** Framework web assíncrono para criar a API REST
- **Celery:** Fila de tarefas distribuída para processamento assíncrono
- **Redis:** Broker de mensagens e backend de resultados
- **yt-dlp:** Ferramenta robusta para busca e download de vídeos do YouTube
- **Pydantic:** Validação de dados e serialização

**Estrutura de Diretórios:**
```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── settings.py          # Configurações centralizadas
│   ├── celery_app.py        # Configuração do Celery
│   ├── tasks.py             # Tarefas Celery
│   ├── models.py            # Modelos Pydantic
│   ├── modules/
│   │   ├── __init__.py
│   │   └── youtube_collector.py  # Lógica de coleta
│   └── api/
│       ├── __init__.py
│       └── collect.py       # Rotas da API
├── .env                     # Configurações
├── requirements.txt         # Dependências Python
└── venv/                    # Ambiente virtual
```

### Frontend

- **React 19:** Biblioteca JavaScript para construir interfaces
- **Vite:** Build tool rápido e moderno
- **Axios:** Cliente HTTP para requisições à API

**Estrutura de Diretórios:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── CollectForm.jsx      # Formulário de coleta
│   │   └── StatusPanel.jsx      # Painel de status
│   ├── styles/
│   │   ├── CollectForm.css      # Estilos do formulário
│   │   └── StatusPanel.css      # Estilos do painel
│   ├── App.jsx                  # Componente principal
│   ├── App.css                  # Estilos globais
│   ├── main.jsx                 # Ponto de entrada
│   └── index.css                # Estilos base
├── package.json                 # Dependências Node.js
├── vite.config.js               # Configuração do Vite
└── node_modules/                # Dependências instaladas
```

## Troubleshooting

### Erro: "Connection refused" ao conectar à API

**Solução:** Certifique-se de que o FastAPI está rodando na porta 8000:
```bash
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Erro: "Redis connection error"

**Solução:** Certifique-se de que o Redis está rodando:
```bash
redis-server
```

### Erro: "Celery worker not responding"

**Solução:** Reinicie o Celery worker:
```bash
cd backend
source venv/bin/activate
celery -A src.celery_app worker --loglevel=info
```

### Tarefa fica em "Aguardando..." indefinidamente

**Solução:** Verifique se o Celery worker está rodando e se o Redis está acessível.

## Notas Importantes

1. **Modo Automático:** Busca vídeos dos últimos 7 dias dos canais GETV e CazeTV.
2. **Retry Automático:** As tarefas têm retry automático com backoff exponencial em caso de falha de rede.
3. **Polling:** O frontend faz polling a cada 3 segundos para atualizar o status da tarefa.
4. **CORS:** A API está configurada para aceitar requisições de qualquer origem (CORS habilitado).

## Próximas Melhorias

- Adicionar autenticação de usuários
- Implementar WebSocket para atualizações em tempo real
- Adicionar suporte para download direto de vídeos
- Implementar filtros mais avançados
- Adicionar histórico de coletas
