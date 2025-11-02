import React, { useState } from 'react';
import axios from 'axios';
import '../styles/DownloadPanel.css';

const DownloadPanel = ({ videoUrl, videoTitle, onDownloadStart, onDownloadProgress, onDownloadComplete }) => {
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [downloadStatus, setDownloadStatus] = useState('');
  const [taskId, setTaskId] = useState(null);
  const [error, setError] = useState(null);
  const [formatChoice, setFormatChoice] = useState('best');

  const startDownload = async () => {
    if (!videoUrl) {
      setError('Por favor, selecione um vídeo para baixar');
      return;
    }

    try {
      setError(null);
      setIsDownloading(true);
      setDownloadProgress(0);
      setDownloadStatus('Iniciando download...');

      // Disparar tarefa de download
      const response = await axios.post('http://localhost:8000/api/v1/download/video', {
        video_url: videoUrl,
        format_choice: formatChoice,
      });

      const newTaskId = response.data.task_id;
      setTaskId(newTaskId);

      if (onDownloadStart) {
        onDownloadStart(newTaskId);
      }

      // Polling para atualizar progresso
      pollDownloadStatus(newTaskId);
    } catch (err) {
      setError(`Erro ao iniciar download: ${err.response?.data?.detail || err.message}`);
      setIsDownloading(false);
    }
  };

  const pollDownloadStatus = async (taskId) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/download/status/${taskId}`);
        const { status, progress, result, error: taskError } = response.data;

        if (status === 'PROGRESS' && progress) {
          const current = progress.current || 0;
          setDownloadProgress(current);
          setDownloadStatus(progress.status || 'Baixando...');

          if (onDownloadProgress) {
            onDownloadProgress(current, progress.status);
          }
        } else if (status === 'SUCCESS') {
          clearInterval(pollInterval);
          setDownloadProgress(100);
          setDownloadStatus('Download concluído com sucesso!');
          setIsDownloading(false);

          if (onDownloadComplete) {
            onDownloadComplete(result);
          }

          // Limpar após 3 segundos
          setTimeout(() => {
            setDownloadProgress(0);
            setDownloadStatus('');
            setTaskId(null);
          }, 3000);
        } else if (status === 'FAILURE') {
          clearInterval(pollInterval);
          setError(`Erro no download: ${taskError}`);
          setIsDownloading(false);
        }
      } catch (err) {
        console.error('Erro ao consultar status:', err);
      }
    }, 1000);
  };

  return (
    <div className="download-panel">
      <div className="download-header">
        <h3>📥 Download de Vídeo</h3>
      </div>

      {error && (
        <div className="error-message">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      <div className="download-form">
        <div className="form-group">
          <label>URL do Vídeo:</label>
          <input
            type="text"
            value={videoUrl}
            readOnly
            placeholder="Selecione um vídeo da busca"
            className="video-url-input"
          />
        </div>

        <div className="form-group">
          <label>Qualidade:</label>
          <select
            value={formatChoice}
            onChange={(e) => setFormatChoice(e.target.value)}
            disabled={isDownloading}
            className="format-select"
          >
            <option value="best">Melhor qualidade (MP4)</option>
            <option value="best[ext=mp4]">Melhor qualidade MP4</option>
            <option value="best[height<=720]">720p</option>
            <option value="best[height<=480]">480p</option>
            <option value="best[height<=360]">360p</option>
            <option value="bestaudio">Apenas áudio</option>
          </select>
        </div>

        <button
          onClick={startDownload}
          disabled={isDownloading || !videoUrl}
          className="download-button"
        >
          {isDownloading ? '⏳ Baixando...' : '📥 Iniciar Download'}
        </button>
      </div>

      {isDownloading && (
        <div className="download-progress">
          <div className="progress-info">
            <span className="progress-label">{downloadStatus}</span>
            <span className="progress-percentage">{downloadProgress}%</span>
          </div>
          <div className="progress-bar-container">
            <div
              className="progress-bar"
              style={{ width: `${downloadProgress}%` }}
            />
          </div>
        </div>
      )}

      {taskId && !isDownloading && (
        <div className="download-complete">
          <span>✅ Download concluído!</span>
        </div>
      )}
    </div>
  );
};

export default DownloadPanel;
