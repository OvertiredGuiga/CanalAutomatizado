# Guia de Usuário - Flamengo AI Creator

## Visão Geral

O **Flamengo AI Creator** é uma aplicação web para coleta automatizada de vídeos do YouTube. A aplicação é dividida em dois componentes principais: um backend robusto (FastAPI + Celery + Redis) e um frontend reativo (React + Vite).

## Pré-requisitos

Escolha o seu sistema operacional abaixo:

### Windows (Nativo)

1. **Instalar Python 3.11+:**
   - Acesse [python.org](https://www.python.org/downloads/)
   - Baixe Python 3.11 ou superior
   - **IMPORTANTE:** Marque a opção "Add Python to PATH" durante a instalação
   - Verifique a instalação:
   ```cmd
   python --version
   ```

2. **Instalar Node.js 18+:**
   - Acesse [nodejs.org](https://nodejs.org/)
   - Baixe a versão LTS
   - Execute o instalador
   - Verifique a instalação:
   ```cmd
   node --version
   npm --version
   ```

3. **Instalar Redis:**
   - Opção 1: Usar Windows Subsystem for Linux (WSL2) - veja seção WSL2 abaixo
   - Opção 2: Usar Docker - [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop)
   - Opção 3: Usar Redis compilado para Windows - [Memurai Redis](https://www.memurai.com/)
   
   **Recomendado: Docker Desktop**
   ```cmd
   # Após instalar Docker Desktop, execute:
   docker run -d -p 6379:6379 redis:latest
   ```

4. **Instalar Git:**
   - Acesse [git-scm.com](https://git-scm.com/)
   - Execute o instalador
   - Verifique a instalação:
   ```cmd
   git --version
   ```

### Linux (Ubuntu/Debian)

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

### WSL2 (Windows Subsystem for Linux)

1. **Instalar WSL2:**
   - Abra PowerShell como administrador e execute:
   ```powershell
   wsl --install
   ```
   - Reinicie o computador
   - Escolha uma distribuição Linux (recomendado: Ubuntu 22.04)

2. **Dentro do WSL2, execute:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip nodejs redis-server git
   ```

3. **Iniciar o Redis no WSL2:**
   ```bash
   sudo service redis-server start
   ```

### macOS

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

A aplicação requer 4 componentes rodando simultaneamente. Abra **4 terminais/prompts diferentes** e siga as instruções para seu sistema operacional.

### Terminal 1: Redis (Broker de Mensagens)

#### Windows (com Docker)

```cmd
# Se não tiver iniciado o Redis com Docker, execute:
docker run -d -p 6379:6379 redis:latest

# Verificar se está rodando:
docker ps
```

#### Windows (com Memurai)

```cmd
# Se instalou via Memurai, o Redis deve estar rodando como serviço
# Verificar status:
sc query memurai

# Se não estiver rodando:
net start memurai
```

#### Linux/WSL2

```bash
# Iniciar o Redis
redis-server

# Saída esperada:
# * Ready to accept connections
```

#### macOS

```bash
# Se instalou via Homebrew
brew services start redis

# Ou manualmente
redis-server
```

**Verificar se está rodando (todos os SOs):**
```
redis-cli ping
# Resposta esperada: PONG
```

**Porta padrão:** `6379`

### Terminal 2: Celery Worker (Processador de Tarefas)

#### Windows

```cmd
# Navegar até o diretório do backend
cd C:\caminho\para\CanalAutomatizado\backend

# Criar ambiente virtual (primeira vez)
python -m venv venv

# Ativar o ambiente virtual
venv\Scripts\activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Iniciar o Celery worker
celery -A src.celery_app worker --loglevel=info

# Saída esperada:
# celery@hostname ready to accept tasks
```

#### Linux/WSL2/macOS

```bash
# Navegar até o diretório do backend
cd /caminho/para/CanalAutomatizado/backend

# Criar ambiente virtual (primeira vez)
python3.11 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Iniciar o Celery worker
celery -A src.celery_app worker --loglevel=info

# Saída esperada:
# celery@hostname ready to accept tasks
```

**Parar o Celery:** `Ctrl + C`

### Terminal 3: FastAPI Backend (Servidor da API)

#### Windows

```cmd
# Navegar até o diretório do backend
cd C:\caminho\para\CanalAutomatizado\backend

# Ativar o ambiente virtual
venv\Scripts\activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Iniciar o servidor FastAPI
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Saída esperada:
# Uvicorn running on http://0.0.0.0:8000
```

#### Linux/WSL2/macOS

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

#### Windows

```cmd
# Navegar até o diretório do frontend
cd C:\caminho\para\CanalAutomatizado\frontend

# Instalar dependências (primeira vez)
npm install

# Iniciar o servidor de desenvolvimento
npm run dev

# Saída esperada:
# ➜  Local:   http://localhost:5173/
```

#### Linux/WSL2/macOS

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

**Notas especiais:**
- **Windows:** Use `localhost` ou `127.0.0.1`
- **WSL2:** Se Redis está no WSL, use `localhost`. Se está no Windows, use o IP do WSL (obtido com `wsl hostname -I`)
- **Docker:** Se Redis está em um container Docker, use `host.docker.internal:6379` (Windows) ou `172.17.0.1:6379` (Linux)

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

### Windows: Erro ao executar Python

**Problema:** `'python' is not recognized as an internal or external command`

**Solução:** 
- Reinstale Python marcando "Add Python to PATH"
- Ou use `python3` em vez de `python`
- Ou adicione Python ao PATH manualmente

### Windows: Erro ao executar npm

**Problema:** `'npm' is not recognized`

**Solução:**
- Reinstale Node.js
- Reinicie o terminal/prompt

### Erro: "Connection refused" ao conectar à API

**Windows:**
```cmd
cd backend
venv\Scripts\activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Linux/WSL2/macOS:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Erro: "Redis connection error"

**Windows (Docker):**
```cmd
# Verificar se Docker está rodando
docker ps

# Se Redis não estiver rodando:
docker run -d -p 6379:6379 redis:latest
```

**Windows (Memurai):**
```cmd
# Verificar status
sc query memurai

# Iniciar se necessário
net start memurai
```

**Linux/WSL2:**
```bash
# Verificar se está rodando
redis-cli ping

# Se não estiver:
redis-server
```

**macOS:**
```bash
# Verificar status
brew services list | grep redis

# Iniciar se necessário
brew services start redis
```

### Erro: "Celery worker not responding"

**Windows:**
```cmd
cd backend
venv\Scripts\activate
celery -A src.celery_app worker --loglevel=info
```

**Linux/WSL2/macOS:**
```bash
cd backend
source venv/bin/activate
celery -A src.celery_app worker --loglevel=info
```

### Tarefa fica em "Aguardando..." indefinidamente

**Solução:** Verifique se:
1. O Celery worker está rodando
2. O Redis está acessível
3. Não há erros nos logs do Celery ou FastAPI

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

# No Windows, acesse no navegador:
# http://<IP-DO-WSL>:5173
```

### Windows: Porta já está em uso

**Problema:** `Address already in use`

**Solução:**
```cmd
# Encontrar qual processo está usando a porta (ex: 8000)
netstat -ano | findstr :8000

# Matar o processo (substitua PID pelo número encontrado)
taskkill /PID <PID> /F

# Ou use portas diferentes:
python -m uvicorn src.main:app --port 8001
npm run dev -- --port 5174
```

## Notas Importantes

1. **Modo Automático:** Busca vídeos dos últimos 7 dias dos canais GETV e CazeTV.
2. **Retry Automático:** As tarefas têm retry automático com backoff exponencial em caso de falha de rede.
3. **Polling:** O frontend faz polling a cada 3 segundos para atualizar o status da tarefa.
4. **CORS:** A API está configurada para aceitar requisições de qualquer origem (CORS habilitado).
5. **Ambiente Virtual:** Sempre ative o ambiente virtual antes de executar comandos Python.

## Script de Inicialização Rápida

### Windows (batch script)

Crie um arquivo `start.bat`:

```batch
@echo off
echo Iniciando Flamengo AI Creator...

REM Verificar se Redis está rodando
docker ps | findstr redis >nul
if errorlevel 1 (
    echo Iniciando Redis com Docker...
    docker run -d -p 6379:6379 redis:latest
    timeout /t 2
)

REM Terminal 1: Celery Worker
echo Iniciando Celery Worker...
start cmd /k "cd backend && venv\Scripts\activate && celery -A src.celery_app worker --loglevel=info"

REM Terminal 2: FastAPI
echo Iniciando FastAPI...
start cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"

REM Terminal 3: Vite
echo Iniciando Vite...
start cmd /k "cd frontend && npm run dev"

echo.
echo Todos os serviços iniciados!
echo Acesse: http://localhost:5173
echo API Docs: http://localhost:8000/docs
```

Salve e execute clicando duas vezes no arquivo.

### Linux/WSL2/macOS (bash script)

Crie um arquivo `start.sh`:

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

Salve e execute:
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
