import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import DashboardStats from './components/DashboardStats';
import AdvancedSearch from './components/AdvancedSearch';
import CollectForm from './components/CollectForm';
import StatusPanel from './components/StatusPanel';
import DownloadPanel from './components/DownloadPanel';
import './App.css';

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [taskId, setTaskId] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);

  const handleCollectStart = (newTaskId) => {
    setTaskId(newTaskId);
    setSearchResults([]);
    setSelectedVideo(null);
  };

  const handleCollectComplete = (results) => {
    console.log('Resultados recebidos:', results);
    
    if (results) {
      let videos = [];
      
      if (results.videos && Array.isArray(results.videos)) {
        videos = results.videos;
      } else if (Array.isArray(results)) {
        videos = results;
      } else if (results.result && results.result.videos) {
        videos = results.result.videos;
      }
      
      console.log('Videos processados:', videos);
      setSearchResults(videos);
    }
  };

  const handleVideoSelect = (video) => {
    setSelectedVideo(video);
  };

  const handleSearch = (query, filters) => {
    console.log('Busca:', query, filters);
    // Aqui você pode integrar com a API de busca
  };

  const handleFilterChange = (filters) => {
    console.log('Filtros alterados:', filters);
  };

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <Sidebar activeSection={activeSection} onSectionChange={setActiveSection} />

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="app-header">
          <div className="header-container">
            <div className="logo-section">
              <img src="/flamengo-shield.png" alt="Flamengo" className="shield-logo" />
              <div className="header-text">
                <h1>🛡️ Flamengo AI Creator</h1>
                <p>Sistema Inteligente de Coleta e Edição de Vídeos</p>
              </div>
            </div>
            <div className="header-badge">v1.0.0</div>
          </div>
        </header>

        {/* Content Area */}
        <div className="content-area">
          {/* Dashboard Section */}
          {activeSection === 'dashboard' && (
            <section className="section-container">
              <DashboardStats />
            </section>
          )}

          {/* Collect Videos Section */}
          {activeSection === 'collect' && (
            <section className="section-container">
              <div className="section-header">
                <h2>🔍 Coletar Vídeos</h2>
                <p>Busque e encontre vídeos do Flamengo</p>
              </div>
              
              <div className="collect-container">
                <div className="collect-left">
                  <CollectForm onTaskCreated={handleCollectStart} />
                </div>

                <div className="collect-right">
                  {/* Status Panel */}
                  {taskId && (
                    <div className="panel-section">
                      <div className="panel-header">
                        <h3>📊 Status da Coleta</h3>
                      </div>
                      <StatusPanel
                        taskId={taskId}
                        onClose={() => setTaskId(null)}
                        onCollectComplete={handleCollectComplete}
                      />
                    </div>
                  )}

                  {/* Search Results */}
                  {searchResults.length > 0 && (
                    <div className="panel-section">
                      <div className="panel-header">
                        <h3>📹 Resultados ({searchResults.length})</h3>
                      </div>
                      <div className="results-grid">
                        {searchResults.map((video, index) => (
                          <div
                            key={index}
                            className={`video-result-card ${selectedVideo?.url === video.url ? 'selected' : ''}`}
                            onClick={() => handleVideoSelect(video)}
                          >
                            <div className="result-thumbnail">
                              {video.thumbnail && (
                                <img src={video.thumbnail} alt={video.title} />
                              )}
                              <div className="play-overlay">▶</div>
                            </div>
                            <div className="result-content">
                              <h4>{video.title}</h4>
                              <p className="result-channel">{video.channel}</p>
                              <div className="result-meta">
                                <span>📅 {new Date(video.published_at).toLocaleDateString('pt-BR')}</span>
                                <span>⏱️ {video.duration}s</span>
                              </div>
                              <a
                                href={video.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="youtube-btn"
                              >
                                YouTube →
                              </a>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Download Panel */}
                  {selectedVideo && (
                    <div className="panel-section">
                      <DownloadPanel
                        videoUrl={selectedVideo.url}
                        videoTitle={selectedVideo.title}
                        onDownloadStart={() => {}}
                        onDownloadProgress={() => {}}
                        onDownloadComplete={() => {
                          alert('✅ Vídeo baixado com sucesso!');
                        }}
                      />
                    </div>
                  )}
                </div>
              </div>
            </section>
          )}

          {/* Downloads Section */}
          {activeSection === 'downloads' && (
            <section className="section-container">
              <div className="section-header">
                <h2>📥 Meus Downloads</h2>
                <p>Histórico e gerenciamento de vídeos baixados</p>
              </div>
              <div className="empty-state">
                <p>📁 Nenhum download realizado ainda</p>
              </div>
            </section>
          )}

          {/* Editor Section */}
          {activeSection === 'editor' && (
            <section className="section-container">
              <div className="section-header">
                <h2>✂️ Editor de Cortes</h2>
                <p>Crie e edite cortes de vídeos com timeline visual</p>
              </div>
              <div className="empty-state">
                <p>🎬 Selecione um vídeo para começar a editar</p>
              </div>
            </section>
          )}

          {/* Templates Section */}
          {activeSection === 'templates' && (
            <section className="section-container">
              <div className="section-header">
                <h2>📋 Templates de Automação</h2>
                <p>Crie vídeos automaticamente usando templates</p>
              </div>
              <div className="templates-grid">
                <div className="template-card">
                  <div className="template-icon">🎬</div>
                  <h3>Intro Profissional</h3>
                  <p>Template de introdução com logo e efeitos</p>
                  <button className="use-template-btn">Usar Template</button>
                </div>
                <div className="template-card">
                  <div className="template-icon">🎵</div>
                  <h3>Com Música</h3>
                  <p>Adicione música de fundo automaticamente</p>
                  <button className="use-template-btn">Usar Template</button>
                </div>
                <div className="template-card">
                  <div className="template-icon">📝</div>
                  <h3>Com Legendas</h3>
                  <p>Gere legendas automáticas para seus vídeos</p>
                  <button className="use-template-btn">Usar Template</button>
                </div>
                <div className="template-card">
                  <div className="template-icon">🎨</div>
                  <h3>Efeitos Visuais</h3>
                  <p>Aplique efeitos e transições profissionais</p>
                  <button className="use-template-btn">Usar Template</button>
                </div>
              </div>
            </section>
          )}

          {/* Analytics Section */}
          {activeSection === 'analytics' && (
            <section className="section-container">
              <div className="section-header">
                <h2>📈 Análises e Relatórios</h2>
                <p>Acompanhe o desempenho dos seus vídeos</p>
              </div>
              <div className="analytics-grid">
                <div className="analytics-card">
                  <h3>👁️ Visualizações</h3>
                  <p className="analytics-value">15.420</p>
                  <p className="analytics-trend">↑ +2.5k este mês</p>
                </div>
                <div className="analytics-card">
                  <h3>👍 Curtidas</h3>
                  <p className="analytics-value">1.240</p>
                  <p className="analytics-trend">↑ +320 esta semana</p>
                </div>
                <div className="analytics-card">
                  <h3>💬 Comentários</h3>
                  <p className="analytics-value">340</p>
                  <p className="analytics-trend">↑ +85 esta semana</p>
                </div>
                <div className="analytics-card">
                  <h3>🔄 Compartilhamentos</h3>
                  <p className="analytics-value">520</p>
                  <p className="analytics-trend">↑ +120 este mês</p>
                </div>
              </div>
            </section>
          )}

          {/* Projects Section */}
          {activeSection === 'projects' && (
            <section className="section-container">
              <div className="section-header">
                <h2>🎬 Meus Projetos</h2>
                <p>Organize seus vídeos em projetos</p>
              </div>
              <div className="empty-state">
                <p>📂 Nenhum projeto criado ainda</p>
                <button className="create-project-btn">+ Novo Projeto</button>
              </div>
            </section>
          )}
        </div>

        {/* Footer */}
        <footer className="app-footer">
          <div className="footer-content">
            <p><strong>🛡️ Flamengo AI Creator</strong> - Sistema Inteligente de Coleta e Edição de Vídeos</p>
            <p className="footer-info">Powered by FastAPI • Celery • React • Vite</p>
            <p className="footer-copyright">© 2025 Flamengo AI Creator. Todos os direitos reservados.</p>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;
