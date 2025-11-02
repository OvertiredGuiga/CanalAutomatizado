import React, { useState } from 'react';
import axios from 'axios';
import '../styles/CollectForm.css';

const CollectForm = ({ onTaskCreated }) => {
  const [mode, setMode] = useState('manual');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedChannels, setSelectedChannels] = useState([]);
  const [filterBy, setFilterBy] = useState('relevance');
  const [timeRange, setTimeRange] = useState('any');
  const [maxDuration, setMaxDuration] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const channels = [
    { id: 'getv', name: 'GETV' },
    { id: 'cazetv', name: 'CazeTV' },
  ];

  const handleChannelToggle = (channelId) => {
    setSelectedChannels((prev) =>
      prev.includes(channelId)
        ? prev.filter((id) => id !== channelId)
        : [...prev, channelId]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const payload = {
        mode: mode,
        search_query: mode === 'manual' ? searchQuery : '',
        channel_ids: selectedChannels.length > 0 ? selectedChannels : null,
        filter_by: filterBy,
        time_range: timeRange,
        max_duration: maxDuration ? parseInt(maxDuration) : null,
      };

      const response = await axios.post(
        'http://localhost:8000/api/v1/collect/youtube',
        payload
      );

      if (response.data && response.data.task_id) {
        onTaskCreated(response.data.task_id);
        // Resetar formulário
        setSearchQuery('');
        setSelectedChannels([]);
        setMaxDuration('');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao iniciar coleta');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="collect-form" onSubmit={handleSubmit}>
      <h2>Formulário de Coleta de Vídeos</h2>

      {error && <div className="error-message">{error}</div>}

      {/* Modo de Coleta */}
      <div className="form-group">
        <label>Modo de Coleta</label>
        <div className="mode-toggle">
          <label className="toggle-label">
            <input
              type="radio"
              value="manual"
              checked={mode === 'manual'}
              onChange={(e) => setMode(e.target.value)}
            />
            Manual
          </label>
          <label className="toggle-label">
            <input
              type="radio"
              value="auto"
              checked={mode === 'auto'}
              onChange={(e) => setMode(e.target.value)}
            />
            Automático
          </label>
        </div>
      </div>

      {/* Query de Busca (apenas para modo manual) */}
      {mode === 'manual' && (
        <div className="form-group">
          <label htmlFor="search-query">Query de Busca</label>
          <input
            id="search-query"
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Ex: Flamengo, Jogo Completo, etc."
            required={mode === 'manual'}
          />
        </div>
      )}

      {/* Canais */}
      <div className="form-group">
        <label>Canais</label>
        <div className="channels-list">
          {channels.map((channel) => (
            <label key={channel.id} className="checkbox-label">
              <input
                type="checkbox"
                checked={selectedChannels.includes(channel.id)}
                onChange={() => handleChannelToggle(channel.id)}
              />
              {channel.name}
            </label>
          ))}
        </div>
      </div>

      {/* Filtro de Busca */}
      {mode === 'manual' && (
        <div className="form-group">
          <label htmlFor="filter-by">Filtrar por</label>
          <select
            id="filter-by"
            value={filterBy}
            onChange={(e) => setFilterBy(e.target.value)}
          >
            <option value="relevance">Relevância</option>
            <option value="date">Data</option>
          </select>
        </div>
      )}

      {/* Intervalo de Tempo */}
      {mode === 'manual' && (
        <div className="form-group">
          <label htmlFor="time-range">Intervalo de Tempo</label>
          <select
            id="time-range"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <option value="any">Qualquer tempo</option>
            <option value="hour">Última hora</option>
            <option value="day">Último dia</option>
            <option value="week">Última semana</option>
            <option value="month">Último mês</option>
            <option value="year">Último ano</option>
          </select>
        </div>
      )}

      {/* Duração Máxima */}
      {mode === 'manual' && (
        <div className="form-group">
          <label htmlFor="max-duration">Duração Máxima (minutos)</label>
          <input
            id="max-duration"
            type="number"
            value={maxDuration}
            onChange={(e) => setMaxDuration(e.target.value)}
            placeholder="Ex: 120"
            min="1"
          />
        </div>
      )}

      {/* Botão de Envio */}
      <button
        type="submit"
        disabled={loading}
        className={`submit-button ${loading ? 'loading' : ''}`}
      >
        {loading ? 'Processando...' : 'Iniciar Coleta'}
      </button>
    </form>
  );
};

export default CollectForm;
