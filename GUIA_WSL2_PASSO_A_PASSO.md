# Guia Passo a Passo - Inicialização no WSL2

## Resumo da Sequência

Você precisa abrir **4 terminais WSL2 diferentes** e iniciar os componentes **nesta ordem exata**:

1. **Terminal 1:** Redis (Broker de Mensagens)
2. **Terminal 2:** Celery Worker (Processador de Tarefas)
3. **Terminal 3:** FastAPI Backend (API REST)
4. **Terminal 4:** Vite Frontend (Interface Web)

---

## Passo 1: Clonar o Repositório

Abra um terminal WSL2 e execute:

```bash
git clone https://github.com/OvertiredGuiga/CanalAutomatizado.git
cd CanalAutomatizado
```

Verifique se os diretórios estão corretos:

```bash
ls -la
# Deve mostrar: backend/ frontend/ userGuide.md README.md CHANGELOG.md
```

---

## Passo 2: Preparar o Ambiente Python (Backend)

Ainda no mesmo terminal, execute:

```bash
cd backend

# Criar ambiente virtual
python3.11 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Voltar para o diretório raiz
cd ..
```

**Saída esperada:**
```
Successfully installed fastapi uvicorn celery redis yt-dlp python-dotenv httpx pydantic pydantic-settings
```

---

## Passo 3: Preparar o Ambiente Node.js (Frontend)

No mesmo terminal, execute:

```bash
cd frontend

# Instalar dependências
npm install

# Voltar para o diretório raiz
cd ..
```

**Saída esperada:**
```
added 152 packages in X seconds
```

---

## Agora Abra 4 Terminais WSL2 Diferentes

Você pode abrir novos terminais WSL2 de várias formas:
- Clique direito no menu Iniciar → Windows Terminal → Nova aba WSL
- Ou use `Ctrl + Shift + 1` no Windows Terminal para nova aba
- Ou abra 4 janelas diferentes do Windows Terminal

---

## Terminal 1: Redis (Broker de Mensagens)

**Neste terminal, execute:**

```bash
# Entrar no diretório do projeto
cd /caminho/para/CanalAutomatizado

# Iniciar Redis
redis-server
```

**Saída esperada:**
```
* Ready to accept connections
```

**Deixe este terminal rodando!** Não feche.

**Verificação (em outro terminal):**
```bash
redis-cli ping
# Resposta: PONG
```

---

## Terminal 2: Celery Worker (Processador de Tarefas)

**Neste novo terminal, execute:**

```bash
# Entrar no diretório do projeto
cd /caminho/para/CanalAutomatizado/backend

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar Celery Worker
celery -A src.celery_app worker --loglevel=info
```

**Saída esperada:**
```
 -------------- celery@hostname v5.5.3 (sun-of-a-gun)
 --- ***** -----
 -- ******* ----
 - *** --- * ---
 - ** ---------- [config]
 - ** ---------- .broker: redis://localhost:6379/0
 - ** ---------- .app: src.celery_app
 - ** ---------- .concurrency: 4 (prefork)
 - ** ---------- [queues]
 - ** ---------- celery
 
 [tasks]
   . src.tasks.collect_youtube_videos

celery@hostname ready to accept tasks
```

**Deixe este terminal rodando!** Não feche.

---

## Terminal 3: FastAPI Backend (API REST)

**Neste novo terminal, execute:**

```bash
# Entrar no diretório do backend
cd /caminho/para/CanalAutomatizado/backend

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar FastAPI
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Deixe este terminal rodando!** Não feche.

**Verificação (em outro terminal):**
```bash
curl http://localhost:8000/health
# Resposta: {"status":"healthy","service":"Flamengo AI Creator - Coleta de Vídeos"}
```

---

## Terminal 4: Vite Frontend (Interface Web)

**Neste novo terminal, execute:**

```bash
# Entrar no diretório do frontend
cd /caminho/para/CanalAutomatizado/frontend

# Iniciar Vite
npm run dev
```

**Saída esperada:**
```
  VITE v7.1.12  ready in 235 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Deixe este terminal rodando!** Não feche.

---

## Acessar a Aplicação

Abra seu navegador **no Windows** e acesse:

```
http://localhost:5173
```

Você verá a interface do **Flamengo AI Creator** com:
- Formulário de coleta de vídeos
- Opções de modo manual/automático
- Painel de status em tempo real

---

## Documentação da API

Para acessar a documentação interativa da API, abra:

```
http://localhost:8000/docs
```

Aqui você pode testar os endpoints diretamente:
- `POST /api/v1/collect/youtube` - Disparar coleta
- `GET /api/v1/collect/status/{task_id}` - Ver status

---

## Resumo dos Terminais

| Terminal | Comando | Porta | Status |
|----------|---------|-------|--------|
| 1 | `redis-server` | 6379 | Deve estar rodando |
| 2 | `celery -A src.celery_app worker --loglevel=info` | - | Deve estar rodando |
| 3 | `python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload` | 8000 | Deve estar rodando |
| 4 | `npm run dev` | 5173 | Deve estar rodando |

---

## Parando a Aplicação

Para parar tudo, em cada terminal pressione:

```
Ctrl + C
```

**Ordem recomendada para parar:**
1. Terminal 4 (Vite)
2. Terminal 3 (FastAPI)
3. Terminal 2 (Celery)
4. Terminal 1 (Redis)

---

## Troubleshooting WSL2

### Erro: "Redis connection refused"

**Solução:**
```bash
# Verificar se Redis está rodando
redis-cli ping

# Se não responder com PONG, inicie Redis no Terminal 1
redis-server
```

### Erro: "Celery worker not responding"

**Solução:**
- Verifique se Redis está rodando (Terminal 1)
- Verifique se está no diretório correto
- Verifique se o ambiente virtual está ativado (`source venv/bin/activate`)

### Erro: "Port already in use"

**Solução:**
```bash
# Para FastAPI (porta 8000)
python -m uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# Para Vite (porta 5173)
npm run dev -- --port 5174
```

### Erro: "Module not found"

**Solução:**
```bash
# Certifique-se de que o ambiente virtual está ativado
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

### WSL2 muito lento

**Solução:**
- Coloque o projeto em `/home/usuario/` em vez de `/mnt/c/`
- Acesse via `\\wsl$\Ubuntu\home\usuario\CanalAutomatizado` no Windows Explorer

---

## Próximos Passos

1. ✅ Todos os 4 componentes rodando
2. ✅ Acesse http://localhost:5173
3. ✅ Teste o formulário de coleta
4. ✅ Veja o painel de status em tempo real
5. ✅ Explore a API em http://localhost:8000/docs

---

## Dúvidas?

Consulte o `userGuide.md` completo para mais detalhes sobre:
- Variáveis de ambiente
- Endpoints da API
- Arquitetura do projeto
- Troubleshooting avançado
