import React, { useState } from 'react';
import CollectForm from './components/CollectForm';
import StatusPanel from './components/StatusPanel';
import DownloadPanel from './components/DownloadPanel';
import './App.css';

function App() {
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

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-container">
          <div className="logo-section">
            <img src="/flamengo-shield.png" alt="Flamengo" className="shield-logo" />
            <div className="header-text">
              <h1>Flamengo AI Creator</h1>
              <p>Sistema Inteligente de Coleta de Vídeos</p>
            </div>
          </div>
          <div className="header-badge">v1.0.0</div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          {/* Left Column - Coleta */}
          <div className="left-column">
            <section className="section">
              <div className="section-header">
                <h2>🔍 Buscar Vídeos</h2>
                <span className="section-subtitle">Pesquise e encontre vídeos do Flamengo</span>
              </div>
              <CollectForm onTaskCreated={handleCollectStart} />
            </section>
          </div>

          {/* Right Column - Status e Resultados */}
          <div className="right-column">
            {/* Status Panel */}
            {taskId && (
              <section className="section">
                <div className="section-header">
                  <h2>📊 Status da Busca</h2>
                </div>
                <StatusPanel
                  taskId={taskId}
                  onClose={() => setTaskId(null)}
                  onCollectComplete={handleCollectComplete}
                />
              </section>
            )}

            {/* Search Results */}
            {searchResults.length > 0 && (
              <section className="section">
                <div className="section-header">
                  <h2>📹 Resultados ({searchResults.length})</h2>
                </div>
                <div className="results-list">
                  {searchResults.map((video, index) => (
                    <div
                      key={index}
                      className={`result-item ${selectedVideo?.url === video.url ? 'selected' : ''}`}
                      onClick={() => handleVideoSelect(video)}
                    >
                      <div className="result-thumbnail">
                        {video.thumbnail && (
                          <img src={video.thumbnail} alt={video.title} />
                        )}
                        <div className="play-icon">▶</div>
                      </div>
                      <div className="result-info">
                        <h4>{video.title}</h4>
                        <p className="result-channel">{video.channel}</p>
                        <div className="result-meta">
                          <span className="meta-item">
                            📅 {new Date(video.published_at).toLocaleDateString('pt-BR')}
                          </span>
                          <span className="meta-item">
                            ⏱️ {video.duration}s
                          </span>
                        </div>
                        <a
                          href={video.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="youtube-link"
                        >
                          Abrir no YouTube →
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Download Panel */}
            {selectedVideo && (
              <section className="section">
                <DownloadPanel
                  videoUrl={selectedVideo.url}
                  videoTitle={selectedVideo.title}
                  onDownloadStart={() => {}}
                  onDownloadProgress={() => {}}
                  onDownloadComplete={() => {
                    alert('✅ Vídeo baixado com sucesso!');
                  }}
                />
              </section>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <p>
            <strong>Flamengo AI Creator</strong> - Sistema Inteligente de Coleta de Vídeos
          </p>
          <p className="footer-info">
            Powered by FastAPI • Celery • React • Vite
          </p>
          <p className="footer-copyright">
            © 2025 Flamengo AI Creator. Todos os direitos reservados.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
