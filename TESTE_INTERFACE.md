# 📋 Plano de Testes - Flamengo AI Creator

## Objetivo
Validar que todos os componentes estão funcionando corretamente, o layout é responsivo, e toda a funcionalidade existente foi preservada.

---

## 1. Testes de Layout e Responsividade

### 1.1 Desktop (1920x1080)
- [ ] Sidebar visível à esquerda (280px)
- [ ] Main content ocupa espaço restante
- [ ] Header com logo e badge visível
- [ ] Footer visível no final
- [ ] Sem sobreposições ou elementos cortados
- [ ] Scroll independente no content-area

### 1.2 Tablet (768x1024)
- [ ] Sidebar ainda visível
- [ ] Conteúdo ajustado para largura menor
- [ ] Grid de templates em 2 colunas
- [ ] Sem overflow horizontal

### 1.3 Mobile (375x667)
- [ ] Sidebar colapsável ou oculta
- [ ] Conteúdo em coluna única
- [ ] Botões e inputs com tamanho adequado
- [ ] Sem elementos cortados

---

## 2. Testes de Navegação

### 2.1 Sidebar Navigation
- [ ] Clique em "Dashboard" → Exibe DashboardStats
- [ ] Clique em "Coletar Vídeos" → Exibe CollectForm + StatusPanel
- [ ] Clique em "Downloads" → Exibe seção de downloads
- [ ] Clique em "Editor de Cortes" → Exibe seção de editor
- [ ] Clique em "Templates" → Exibe grid de templates
- [ ] Clique em "Análises" → Exibe cards de analytics
- [ ] Clique em "Projetos" → Exibe seção de projetos
- [ ] Item ativo destacado em vermelho Flamengo

---

## 3. Testes de Componentes

### 3.1 DashboardStats
- [ ] Componente renderiza sem erros
- [ ] Exibe estatísticas
- [ ] Cards com hover effect
- [ ] Cores Flamengo aplicadas

### 3.2 CollectForm
- [ ] Input de busca funciona
- [ ] Botão de busca clicável
- [ ] Modo manual vs automático selecionável
- [ ] Integração com API funcionando

### 3.3 StatusPanel
- [ ] Aparece quando task_id é definido
- [ ] Exibe status da coleta
- [ ] Atualiza em tempo real
- [ ] Botão de fechar funciona

### 3.4 DownloadPanel
- [ ] Aparece quando vídeo é selecionado
- [ ] Exibe opções de qualidade
- [ ] Botão de download funciona
- [ ] Progresso é exibido

### 3.5 Sidebar
- [ ] Logo e título visíveis
- [ ] Botão de colapso funciona
- [ ] Menu items com ícones
- [ ] Footer com versão

---

## 4. Testes de Funcionalidade

### 4.1 Busca de Vídeos
- [ ] Digitar query e clicar em buscar
- [ ] Resultados aparecem em grid
- [ ] Thumbnails carregam
- [ ] Clique em vídeo o seleciona
- [ ] Link YouTube abre em nova aba

### 4.2 Download
- [ ] Selecionar vídeo
- [ ] DownloadPanel aparece
- [ ] Escolher qualidade
- [ ] Clicar em download
- [ ] Progresso é exibido
- [ ] Mensagem de sucesso aparece

### 4.3 Status em Tempo Real
- [ ] Iniciar coleta
- [ ] StatusPanel atualiza
- [ ] Percentual aumenta
- [ ] Status muda de "processando" para "completo"

---

## 5. Testes de Design

### 5.1 Cores Flamengo
- [ ] Vermelho #c22a1e usado em:
  - [ ] Sidebar border
  - [ ] Botões principais
  - [ ] Links ativos
  - [ ] Badges
  - [ ] Hover effects

- [ ] Preto #000000 usado em:
  - [ ] Sidebar background
  - [ ] Texto principal
  - [ ] Borders

### 5.2 Animações
- [ ] Fade in ao trocar seção
- [ ] Slide in dos painéis
- [ ] Hover effects nos cards
- [ ] Transições suaves (0.3s)

### 5.3 Tipografia
- [ ] Headers em tamanho apropriado
- [ ] Texto legível em todos os backgrounds
- [ ] Espaçamento consistente

---

## 6. Testes de Performance

### 6.1 Carregamento
- [ ] Página carrega em < 3s
- [ ] Sem console errors
- [ ] Sem console warnings

### 6.2 Interatividade
- [ ] Cliques respondem imediatamente
- [ ] Scroll suave
- [ ] Sem lag ao trocar seção

---

## 7. Testes de Integração

### 7.1 Backend
- [ ] API de coleta responde
- [ ] API de download responde
- [ ] Status updates funcionam
- [ ] Erros são tratados

### 7.2 Frontend-Backend
- [ ] Requisições são enviadas corretamente
- [ ] Respostas são processadas
- [ ] Dados aparecem na UI

---

## Checklist Final

- [ ] Todos os testes de layout passaram
- [ ] Todos os testes de navegação passaram
- [ ] Todos os testes de componentes passaram
- [ ] Todos os testes de funcionalidade passaram
- [ ] Todos os testes de design passaram
- [ ] Todos os testes de performance passaram
- [ ] Todos os testes de integração passaram
- [ ] Nenhum console error ou warning
- [ ] Aplicação pronta para produção

---

## Notas de Teste

**Data do Teste:** _______________
**Testador:** _______________
**Ambiente:** WSL2 / Windows / Linux / macOS
**Navegador:** Chrome / Firefox / Safari / Edge
**Resolução:** _______________

**Problemas Encontrados:**
1. _______________
2. _______________
3. _______________

**Observações:**
_______________
_______________
_______________

---

## Status Geral

- [ ] ✅ APROVADO - Pronto para produção
- [ ] ⚠️ PARCIAL - Alguns ajustes necessários
- [ ] ❌ REPROVADO - Problemas críticos encontrados

