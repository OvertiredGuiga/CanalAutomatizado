# Histórico de Alterações (Changelog)

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), e o projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-11-01

### Adicionado

- **Backend (FastAPI + Celery + Redis):**
  - API REST com endpoints para coleta de vídeos
  - Modo manual: Busca personalizada com filtros por relevância, data, duração
  - Modo automático: Busca automática de "Jogo Completo" e "Melhores Momentos"
  - Tarefas Celery com retry automático e backoff exponencial
  - Tratamento robusto de erros com logging
  - Validação de requisições com Pydantic
  - Integração com yt-dlp para busca de vídeos

- **Frontend (React + Vite):**
  - Componente CollectForm para formulário de coleta
  - Componente StatusPanel para exibição de status em tempo real
  - Polling eficiente a cada 3 segundos
  - Interface reativa com feedback imediato
  - Design responsivo com CSS moderno
  - Integração com API via Axios

- **Documentação:**
  - userGuide.md com instruções completas de inicialização
  - CONTRIBUTING.md com padrões de commit (Conventional Commits)
  - README.md com visão geral do projeto
  - Comentários detalhados no código

- **Configuração:**
  - Arquivo .env para configurações centralizadas
  - requirements.txt para dependências Python
  - package.json para dependências Node.js
  - .gitignore para exclusão de arquivos desnecessários

## [Não Lançado]

### Planejado

- Autenticação de usuários
- WebSocket para atualizações em tempo real
- Download direto de vídeos
- Filtros mais avançados
- Histórico de coletas
