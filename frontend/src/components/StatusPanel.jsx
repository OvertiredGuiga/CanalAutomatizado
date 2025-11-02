import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/StatusPanel.css';

const StatusPanel = ({ taskId, onClose }) => {
  const [status, setStatus] = useState('PENDING');
  const [progress, setProgress] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!taskId) return;

    const pollStatus = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/v1/collect/status/${taskId}`
        );

        const { status: newStatus, progress: newProgress, result: newResult, error: newError } = response.data;

        setStatus(newStatus);
        setProgress(newProgress);
        setResult(newResult);
        setError(newError);
        setLoading(false);

        // Se a tarefa ainda está em progresso, continuar polling
        if (newStatus === 'PENDING' || newStatus === 'PROGRESS') {
          setTimeout(pollStatus, 3000); // Polling a cada 3 segundos
        }
      } catch (err) {
        console.error('Erro ao consultar status:', err);
        setError('Erro ao consultar status da tarefa');
        setLoading(false);
      }
    };

    pollStatus();
  }, [taskId]);

  const getStatusColor = () => {
    switch (status) {
      case 'PENDING':
      case 'PROGRESS':
        return 'status-progress';
      case 'SUCCESS':
        return 'status-success';
      case 'FAILURE':
        return 'status-failure';
      default:
        return 'status-unknown';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'PENDING':
        return 'Aguardando...';
      case 'PROGRESS':
        return 'Processando...';
      case 'SUCCESS':
        return 'Concluído!';
      case 'FAILURE':
        return 'Falhou';
      default:
        return status;
    }
  };

  return (
    <div className="status-panel">
      <div className="panel-header">
        <h3>Status da Coleta</h3>
        <button className="close-button" onClick={onClose}>
          ✕
        </button>
      </div>

      <div className="panel-content">
        {/* Task ID */}
        <div className="info-row">
          <label>ID da Tarefa:</label>
          <span className="task-id">{taskId}</span>
        </div>

        {/* Status */}
        <div className="info-row">
          <label>Status:</label>
          <span className={`status-badge ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </div>

        {/* Progresso */}
        {progress && (
          <div className="progress-section">
            <label>Progresso:</label>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${(progress.current / progress.total) * 100}%` }}
              ></div>
            </div>
            <p className="progress-text">
              {progress.current} / {progress.total} - {progress.status}
            </p>
          </div>
        )}

        {/* Resultado */}
        {result && status === 'SUCCESS' && (
          <div className="result-section">
            <h4>Resultado da Coleta</h4>
            <p>
              <strong>Total de Vídeos:</strong> {result.total_videos}
            </p>
            {result.videos && result.videos.length > 0 && (
              <div className="videos-list">
                <h5>Vídeos Encontrados:</h5>
                <ul>
                  {result.videos.slice(0, 5).map((video, index) => (
                    <li key={index}>
                      <strong>{video.title}</strong>
                      <br />
                      <small>Canal: {video.channel}</small>
                      <br />
                      <small>
                        <a href={video.url} target="_blank" rel="noopener noreferrer">
                          Abrir no YouTube
                        </a>
                      </small>
                    </li>
                  ))}
                </ul>
                {result.videos.length > 5 && (
                  <p className="more-videos">
                    ... e mais {result.videos.length - 5} vídeos
                  </p>
                )}
              </div>
            )}
          </div>
        )}

        {/* Erro */}
        {error && (
          <div className="error-section">
            <h4>Erro</h4>
            <p>{error}</p>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="loading-section">
            <p>Carregando...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatusPanel;
