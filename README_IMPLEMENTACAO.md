# Implementação da Detecção de Cenas com PySceneDetect

Este documento detalha as modificações realizadas no projeto **CanalAutomatizado** para integrar a funcionalidade de detecção automática de cenas, conforme a pesquisa fornecida.

## 1. Backend (FastAPI + Celery)

A integração do PySceneDetect foi realizada no backend, utilizando o Celery para processamento assíncrono, o que é crucial para tarefas intensivas como a análise de vídeo.

### 1.1. Dependências

A dependência `scenedetect[opencv]` foi adicionada ao `backend/requirements.txt`:

```
scenedetect[opencv]
```

### 1.2. Padronização de Nomes de Arquivo (Correção de Bug)

Para evitar problemas com o PySceneDetect, que não lida bem com espaços no nome do arquivo, a lógica de nomeação foi padronizada:

- **Download de Vídeos (yt-dlp):**
    - **Arquivo:** `backend/src/modules/youtube_downloader.py`
    - **Mudança:** O template de saída (`outtmpl`) do `yt-dlp` foi alterado de `%(title)s.%(ext)s` para `%(id)s.%(ext)s`. Isso garante que os vídeos baixados sejam nomeados apenas com o ID do YouTube, que é único e não contém espaços.

- **Upload de Vídeos (FastAPI):**
    - **Arquivo:** `backend/src/api/scene_detection.py`
    - **Mudança:** A lógica de salvamento de arquivos temporários foi atualizada para remover espaços e caracteres especiais do nome do arquivo original, substituindo-os por underscores (`_`), garantindo um nome de arquivo seguro para o PySceneDetect.

### 1.3. Módulo `SceneDetector`

A dependência `scenedetect[opencv]` foi adicionada ao `backend/requirements.txt`:

```
scenedetect[opencv]
```

### 1.2. Módulo `SceneDetector`

- **Arquivo:** `backend/src/modules/scene_detector.py`
- **Descrição:** Criação de uma classe wrapper para o PySceneDetect, encapsulando a lógica de detecção de cenas (`detect_scenes`) usando os detectores `AdaptiveDetector` e `ContentDetector`.

### 1.3. Tarefa Celery

- **Arquivo:** `backend/src/tasks_scene_detection.py`
- **Descrição:** Criação da tarefa `detect_scenes_task` que recebe o caminho do vídeo e os parâmetros de detecção. Esta tarefa executa o `SceneDetector` e retorna a lista de cenas detectadas (timestamps e frames) em um formato serializável (JSON).

### 1.4. Endpoints FastAPI

- **Arquivo:** `backend/src/api/scene_detection.py`
- **Descrição:** Criação de uma nova rota (`/scene-detection`) com dois endpoints:
    - `POST /scene-detection/detect`: Recebe o arquivo de vídeo via `UploadFile`, salva-o temporariamente e enfileira a `detect_scenes_task` no Celery. Retorna o `task_id`.
    - `GET /scene-detection/status/{task_id}`: Permite acompanhar o status da tarefa Celery. Em caso de sucesso, retorna a lista de cenas e **remove o arquivo temporário** do servidor.

### 1.5. Integração Principal

- **Arquivo:** `backend/src/main.py`
- **Descrição:** A nova rota `scene_detection_router` foi importada e incluída na aplicação FastAPI.

## 2. Frontend (React + Vite)

A dashboard foi aprimorada para permitir o upload de vídeos e a visualização dos resultados da detecção de cenas.

### 2.1. Componente `Sidebar`

- **Arquivo:** `frontend/src/components/Sidebar.jsx`
- **Descrição:** Adicionada uma nova seção no menu de navegação: **"Detecção de Cenas"** (`id: 'scene-detection'`).

### 2.2. Componente `SceneDetectionPanel`

- **Arquivos:** 
    - `frontend/src/components/SceneDetectionPanel.jsx`
    - `frontend/src/styles/SceneDetectionPanel.css`
- **Descrição:** Novo componente que implementa a interface de usuário:
    - **Formulário de Upload:** Permite selecionar um arquivo de vídeo e configurar os parâmetros de detecção (`method`, `adaptive_threshold`, `content_threshold`).
    - **Comunicação com a API:** Envia o vídeo para o endpoint `POST /scene-detection/detect` e, em seguida, faz polling no endpoint `GET /scene-detection/status/{task_id}` para acompanhar o progresso.
    - **Visualização de Resultados:** Exibe a lista de cenas detectadas com seus tempos de início, fim e duração.

### 2.3. Integração Principal

- **Arquivo:** `frontend/src/App.jsx`
- **Descrição:** O `SceneDetectionPanel` foi importado e adicionado à lógica de renderização para ser exibido quando a seção **"Detecção de Cenas"** estiver ativa.

## 3. Pré-requisitos para Execução

Para rodar o projeto com a nova funcionalidade, é necessário garantir que:

1.  **FFmpeg** esteja instalado no ambiente (necessário para o PySceneDetect).
2.  O **Backend** (`FastAPI`) esteja rodando.
3.  O **Celery Worker** esteja rodando e conectado ao Redis.
4.  O **Frontend** (`Vite`) esteja rodando.

### Comandos de Inicialização (Exemplo no WSL2)

1.  **Redis (Broker/Backend do Celery):**
    ```bash
    redis-server
    ```
2.  **Celery Worker (no diretório `backend`):**
    ```bash
    celery -A src.celery_app worker -l info
    ```
3.  **FastAPI (no diretório `backend`):**
    ```bash
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    ```
4.  **Vite Frontend (no diretório `frontend`):**
    ```bash
    pnpm run dev
    ```

A nova funcionalidade estará acessível na dashboard, na seção **"Detecção de Cenas"**.
