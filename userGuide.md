# Guia de Usuário - Flamengo AI Creator

## Visão Geral

O **Flamengo AI Creator** é uma aplicação web para coleta automatizada de vídeos do YouTube. A aplicação é dividida em dois componentes principais: um backend robusto (FastAPI + Celery + Redis) e um frontend reativo (React + Vite).

## Pré-requisitos

### Para Linux (Ubuntu/Debian)

```bash
# Atualizar repositórios
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.11+
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Instalar Node.js 18+ (via NodeSource)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Instalar Redis
sudo apt install -y redis-server

# Instalar Git
sudo apt install -y git
```

### Para WSL2 (Windows Subsystem for Linux)

1. **Instalar WSL2:**
   - Abra PowerShell como administrador e execute:
   ```powershell
   wsl --install
   ```
   - Reinicie o computador
   - Escolha uma distribuição Linux (recomendado: Ubuntu 22.04)

2. **Dentro do WSL2, execute os mesmos comandos do Linux acima:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip nodejs redis-server git
   ```

3. **Iniciar o Redis no WSL2:**
   ```bash
   sudo service redis-server start
   ```

### Para macOS

```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python 3.11+
brew install python@3.11

# Instalar Node.js
brew install node

# Instalar Redis
brew install redis

# Iniciar Redis
brew services start redis
```

## Inicialização dos Componentes

A aplicação requer 4 componentes rodando simultaneamente. Abra **4 terminais diferentes** e siga as instruções abaixo.

### Terminal 1: Redis (Broker de Mensagens)

**Linux/WSL:**
```bash
# Iniciar o Redis
redis-server

# Saída esperada:
# * Ready to accept connections
```

**macOS:**
```bash
# Se instalou via Homebrew
brew services start redis

# Ou manualmente
redis-server
```

**Verificar se está rodando:**
```bash
redis-cli ping
# Resposta esperada: PONG
```

**Porta padrão:** `6379`

### Terminal 2: Celery Worker (Processador de Tarefas)

**Linux/WSL/macOS:**
```bash
# Navegar até o diretório do backend
cd /caminho/para/CanalAutomatizado/backend

# Ativar o ambiente virtual
source venv/bin/activate

# Iniciar o Celery worker
celery -A src.celery_app worker --loglevel=info

# Saída esperada:
# celery@hostname ready to accept tasks
```

**Parar o Celery:** `Ctrl + C`

### Terminal 3: FastAPI Backend (Servidor da API)

**Linux/WSL/macOS:**
```bash
# Navegar até o diretório do backend
cd /caminho/para/CanalAutomatizado/backend

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Iniciar o servidor FastAPI
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Saída esperada:
# Uvicorn running on http://0.0.0.0:8000
```

**Porta padrão:** `8000`
**Documentação da API:** `http://localhost:8000/docs`
**Parar o servidor:** `Ctrl + C`

### Terminal 4: Vite Frontend (Aplicação Web)

**Linux/WSL/macOS:**
```bash
# Navegar até o diretório do frontend
cd /caminho/para/CanalAutomatizado/frontend

# Instalar dependências (primeira vez)
npm install

# Iniciar o servidor de desenvolvimento
npm run dev

# Saída esperada:
# ➜  Local:   http://localhost:5173/
```

**Porta padrão:** `5173`
**URL da aplicação:** `http://localhost:5173`
**Parar o servidor:** `Ctrl + C`

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

**Nota:** Se estiver usando WSL2 e o Redis está rodando no WSL, use `localhost` ou `127.0.0.1`. Se estiver rodando no Windows, use o IP do WSL (obtido com `wsl hostname -I`).

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

**Linux/WSL:**
```bash
# Verificar se o Redis está rodando
redis-cli ping
# Resposta esperada: PONG

# Se não estiver rodando, inicie:
redis-server
```

**macOS:**
```bash
# Verificar status
brew services list | grep redis

# Se não estiver rodando:
brew services start redis
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

### WSL2: Redis não inicia automaticamente

**Solução:** Inicie manualmente em cada sessão:
```bash
sudo service redis-server start
```

Para iniciar automaticamente, adicione ao arquivo `~/.bashrc`:
```bash
sudo service redis-server start 2>/dev/null
```

### WSL2: Conectar do Windows ao servidor rodando no WSL

Se quiser acessar a aplicação do navegador do Windows:
```bash
# No WSL, obtenha o IP
wsl hostname -I

# No Windows, acesse:
# http://<IP-DO-WSL>:5173
```

## Notas Importantes

1. **Modo Automático:** Busca vídeos dos últimos 7 dias dos canais GETV e CazeTV.
2. **Retry Automático:** As tarefas têm retry automático com backoff exponencial em caso de falha de rede.
3. **Polling:** O frontend faz polling a cada 3 segundos para atualizar o status da tarefa.
4. **CORS:** A API está configurada para aceitar requisições de qualquer origem (CORS habilitado).
5. **Ambiente Virtual:** Sempre ative o ambiente virtual antes de executar comandos Python.

## Script de Inicialização Rápida (Linux/WSL)

Para facilitar a inicialização, crie um script `start.sh`:

```bash
#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando Flamengo AI Creator...${NC}"

# Verificar se Redis está rodando
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${YELLOW}Iniciando Redis...${NC}"
    redis-server --daemonize yes
    sleep 2
fi

# Terminal 1: Celery Worker
echo -e "${GREEN}Iniciando Celery Worker...${NC}"
cd backend
source venv/bin/activate
celery -A src.celery_app worker --loglevel=info &
CELERY_PID=$!

# Terminal 2: FastAPI
echo -e "${GREEN}Iniciando FastAPI...${NC}"
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &
FASTAPI_PID=$!

# Terminal 3: Vite
echo -e "${GREEN}Iniciando Vite...${NC}"
cd ../frontend
npm run dev &
VITE_PID=$!

echo -e "${GREEN}Todos os serviços iniciados!${NC}"
echo -e "${YELLOW}Acesse: http://localhost:5173${NC}"
echo -e "${YELLOW}API Docs: http://localhost:8000/docs${NC}"

# Aguardar Ctrl+C
trap "kill $CELERY_PID $FASTAPI_PID $VITE_PID" EXIT
wait
```

Salve como `start.sh` e execute:
```bash
chmod +x start.sh
./start.sh
```

## Próximas Melhorias

- Adicionar autenticação de usuários
- Implementar WebSocket para atualizações em tempo real
- Adicionar suporte para download direto de vídeos
- Implementar filtros mais avançados
- Adicionar histórico de coletas
