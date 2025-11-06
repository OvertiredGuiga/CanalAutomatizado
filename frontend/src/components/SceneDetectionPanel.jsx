import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/SceneDetectionPanel.css'; // Criaremos este arquivo de estilo

const API_BASE_URL = 'http://localhost:8000/scene-detection'; // Assumindo que a API está na porta 8000

const SceneDetectionPanel = () => {
  const [file, setFile] = useState(null);
  const [method, setMethod] = useState('adaptive');
  const [adaptiveThreshold, setAdaptiveThreshold] = useState(3.0);
  const [contentThreshold, setContentThreshold] = useState(27.0);
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);
  const [scenes, setScenes] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setScenes([]);
    setTaskStatus(null);
    setTaskId(null);
    setError(null);
  };

  const handleDetectScenes = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Por favor, selecione um arquivo de vídeo.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setScenes([]);
    setTaskStatus(null);
    setTaskId(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('method', method);
    formData.append('adaptive_threshold', adaptiveThreshold);
    formData.append('content_threshold', contentThreshold);

    try {
      const response = await axios.post(`${API_BASE_URL}/detect`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      const newTaskId = response.data.task_id;
      setTaskId(newTaskId);
      setTaskStatus(response.data.message);
      setIsLoading(false);
    } catch (err) {
      console.error('Erro ao iniciar detecção de cenas:', err);
      setError('Erro ao iniciar detecção de cenas. Verifique o console.');
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let interval;

    if (taskId && taskStatus !== 'SUCCESS' && taskStatus !== 'FAILURE') {
      interval = setInterval(async () => {
        try {
          const response = await axios.get(`${API_BASE_URL}/status/${taskId}`);
          const data = response.data;
          
          setTaskStatus(data.status);

          if (data.status === 'SUCCESS') {
            setScenes(data.result.scenes);
            clearInterval(interval);
          } else if (data.status === 'FAILURE') {
            setError(data.error || 'A tarefa falhou.');
            clearInterval(interval);
          } else if (data.status === 'PROGRESS') {
            setTaskStatus(`Processando: ${data.progress}% - ${data.status_message}`);
          }
        } catch (err) {
          console.error('Erro ao verificar status da tarefa:', err);
          setError('Erro ao verificar status da tarefa.');
          clearInterval(interval);
        }
      }, 3000); // Verifica a cada 3 segundos
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [taskId, taskStatus]);

  const formatTime = (seconds) => {
    const date = new Date(0);
    date.setSeconds(seconds);
    return date.toISOString().substr(11, 8);
  };

  return (
    <div className="scene-detection-panel">
      <div className="detection-form-container">
        <form onSubmit={handleDetectScenes} className="detection-form">
          <div className="form-group">
            <label htmlFor="video-file">Selecione o Vídeo:</label>
            <input
              type="file"
              id="video-file"
              accept="video/*"
              onChange={handleFileChange}
              required
            />
            {file && <p className="file-info">Arquivo selecionado: <strong>{file.name}</strong></p>}
          </div>

          <div className="form-group">
            <label htmlFor="method">Método de Detecção:</label>
            <select
              id="method"
              value={method}
              onChange={(e) => setMethod(e.target.value)}
            >
              <option value="adaptive">AdaptiveDetector (Recomendado para Esportes)</option>
              <option value="content">ContentDetector (Cortes Rápidos)</option>
            </select>
          </div>

          {method === 'adaptive' && (
            <div className="form-group">
              <label htmlFor="adaptive-threshold">Adaptive Threshold:</label>
              <input
                type="number"
                id="adaptive-threshold"
                value={adaptiveThreshold}
                onChange={(e) => setAdaptiveThreshold(parseFloat(e.target.value))}
                step="0.1"
                min="0.1"
              />
              <small>Sensibilidade do AdaptiveDetector (padrão: 3.0)</small>
            </div>
          )}

          {method === 'content' && (
            <div className="form-group">
              <label htmlFor="content-threshold">Content Threshold:</label>
              <input
                type="number"
                id="content-threshold"
                value={contentThreshold}
                onChange={(e) => setContentThreshold(parseFloat(e.target.value))}
                step="1.0"
                min="1.0"
              />
              <small>Sensibilidade do ContentDetector (padrão: 27.0)</small>
            </div>
          )}

          <button type="submit" className="detect-btn" disabled={isLoading || !file}>
            {isLoading ? 'Iniciando...' : '✂️ Iniciar Detecção de Cenas'}
          </button>
        </form>
      </div>

      <div className="detection-status-container">
        <h3>Status da Tarefa</h3>
        {taskId && <p><strong>ID da Tarefa:</strong> {taskId}</p>}
        {taskStatus && <p><strong>Status:</strong> {taskStatus}</p>}
        {error && <p className="error-message"><strong>Erro:</strong> {error}</p>}

        {scenes.length > 0 && (
          <div className="scenes-results">
            <h3>✅ {scenes.length} Cenas Detectadas</h3>
            <div className="scenes-list">
              {scenes.map((scene, index) => (
                <div key={index} className="scene-item">
                  <p><strong>Cena {index + 1}:</strong></p>
                  <p>Início: {formatTime(scene.start_time)} (Frame: {scene.start_frame})</p>
                  <p>Fim: {formatTime(scene.end_time)} (Frame: {scene.end_frame})</p>
                  <p>Duração: {scene.duration.toFixed(2)}s</p>
                </div>
              ))}
            </div>
            <button className="download-scenes-btn" onClick={() => alert('Funcionalidade de download de clipes a ser implementada.')}>
                📥 Baixar Clipes (Em Breve)
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SceneDetectionPanel;
