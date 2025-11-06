# Apresentação: Fluxo de Trabalho de Detecção de Cenas

## 1. Introdução: O Poder da Detecção de Cenas

**Título:** Automatizando a Edição: Integração PySceneDetect
**Subtítulo:** Fluxo de Trabalho para Detecção e Segmentação de Vídeos
**Autor:** Manus AI

---

## 2. Fluxo de Trabalho Ponta a Ponta

**Título:** Processo de Detecção de Cenas
**Conteúdo:**
O fluxo de trabalho é projetado para ser robusto e assíncrono, garantindo que o processamento de vídeos longos não bloqueie a aplicação principal (FastAPI).

1.  **Frontend (Dashboard):** O usuário inicia o processo de detecção de cenas através do painel.
2.  **Upload/Download:** O vídeo é carregado (upload) ou baixado (yt-dlp) para o servidor.
3.  **FastAPI (Endpoint):** O endpoint recebe o arquivo/URL e imediatamente enfileira uma tarefa no Celery.
4.  **Celery (Worker):** O worker executa a tarefa em *background*, utilizando o PySceneDetect.
5.  **PySceneDetect:** Analisa o vídeo e retorna os *timestamps* das transições de cena.
6.  **Resultado:** O resultado é armazenado e exibido na dashboard para o usuário.

---

## 3. Backend: Processamento Assíncrono e Robustez

**Título:** FastAPI, Celery e PySceneDetect
**Conteúdo:**
A arquitetura utiliza o Celery para processamento em *background*, liberando o FastAPI para responder rapidamente ao usuário.

*   **Módulo `SceneDetector`:** Uma classe Python encapsula a lógica do PySceneDetect, permitindo a escolha entre diferentes detectores (ex: `ContentDetector` ou `AdaptiveDetector`).
*   **Tarefa Celery (`detect_scenes_task`):** Recebe o caminho do arquivo de vídeo e os parâmetros de detecção. O Celery gerencia o tempo de execução e o status da tarefa.
*   **Comunicação:** O FastAPI expõe um endpoint para **iniciar** a detecção e outro para **consultar o status** da tarefa (via `task_id` do Celery).

---

## 4. Ponto Crítico: Padronização de Nomes de Arquivo

**Título:** Solução para Restrição de Nomes de Arquivo
**Conteúdo:**
O PySceneDetect e ferramentas como o FFmpeg não suportam nomes de arquivo com espaços ou caracteres especiais, o que causava falhas no processamento.

| Cenário | Problema | Solução Implementada |
| :--- | :--- | :--- |
| **Vídeos Baixados (yt-dlp)** | Títulos longos e com caracteres especiais. | Alterado o template de saída do `yt-dlp` para usar o **ID do Vídeo** (ex: `%(id)s.%(ext)s`), que é um identificador seguro e sem espaços. |
| **Vídeos Enviados (Upload)** | Nomes de arquivo originais do usuário com espaços. | O endpoint de upload agora **sanitiza** o nome do arquivo, substituindo espaços e caracteres não-seguros por *underscores* (`_`) antes de salvar o arquivo temporário. |

**Resultado:** O processamento do PySceneDetect agora é estável, independentemente da origem do vídeo.

---

## 5. Interação com a Dashboard (Frontend)

**Título:** Experiência do Usuário no Painel
**Conteúdo:**
O novo painel de **Detecção de Cenas** oferece controle total sobre o processo:

*   **Upload/Seleção:** Permite o upload de um novo vídeo ou a seleção de um vídeo já baixado.
*   **Parâmetros:** O usuário pode escolher o tipo de detector (`Content` ou `Adaptive`) e ajustar o *threshold* (limiar) de sensibilidade.
*   **Status em Tempo Real:** A dashboard exibe o status atual da tarefa (Enfileirada, Em Progresso, Sucesso ou Falha) usando o `task_id` do Celery.
*   **Resultados:** Em caso de sucesso, é exibida uma lista clara com os *timestamps* de **Início**, **Fim** e **Duração** de cada cena detectada.

---

## 6. Próximos Passos

**Título:** O que vem a seguir?
**Conteúdo:**
Com a detecção de cenas funcionando, o próximo passo lógico é utilizar esses dados:

*   **Editor de Cortes:** Desenvolver a funcionalidade para que o usuário possa selecionar cenas da lista e gerar automaticamente o corte final do vídeo (usando FFmpeg).
*   **Automação:** Integrar a detecção de cenas ao fluxo de trabalho de coleta automática, permitindo que o sistema filtre e processe apenas as cenas mais relevantes.

**Obrigado!**
**Perguntas?**
