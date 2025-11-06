import React, { useState } from 'react';
import '../styles/AdvancedSearch.css';

const AdvancedSearch = ({ onSearch, onFilterChange }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    type: 'all',
    duration: 'all',
    date: 'all',
    quality: 'all',
    channel: 'all',
  });

  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch(searchQuery, filters);
  };

  const handleFilterChange = (filterName, value) => {
    const newFilters = { ...filters, [filterName]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const resetFilters = () => {
    setSearchQuery('');
    setFilters({
      type: 'all',
      duration: 'all',
      date: 'all',
      quality: 'all',
      channel: 'all',
    });
  };

  return (
    <div className="advanced-search">
      <div className="search-header">
        <h3>🔍 Busca Avançada</h3>
        <button 
          className="toggle-advanced"
          onClick={() => setShowAdvanced(!showAdvanced)}
        >
          {showAdvanced ? '▼ Ocultar' : '▶ Mostrar'} Filtros
        </button>
      </div>

      <form onSubmit={handleSearch} className="search-form">
        {/* Main Search Box */}
        <div className="search-box-container">
          <input
            type="text"
            className="search-input"
            placeholder="Buscar vídeos, canais, palavras-chave..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="search-btn">
            <span>🔍</span> Buscar
          </button>
        </div>

        {/* Advanced Filters */}
        {showAdvanced && (
          <div className="filters-container">
            {/* Type Filter */}
            <div className="filter-group">
              <label>Tipo de Vídeo</label>
              <select
                value={filters.type}
                onChange={(e) => handleFilterChange('type', e.target.value)}
                className="filter-select"
              >
                <option value="all">Todos os tipos</option>
                <option value="jogo">Jogo Completo</option>
                <option value="melhores">Melhores Momentos</option>
                <option value="resumo">Resumo</option>
                <option value="entrevista">Entrevista</option>
              </select>
            </div>

            {/* Duration Filter */}
            <div className="filter-group">
              <label>Duração</label>
              <select
                value={filters.duration}
                onChange={(e) => handleFilterChange('duration', e.target.value)}
                className="filter-select"
              >
                <option value="all">Qualquer duração</option>
                <option value="short">Curto (0-5 min)</option>
                <option value="medium">Médio (5-30 min)</option>
                <option value="long">Longo (30+ min)</option>
              </select>
            </div>

            {/* Date Filter */}
            <div className="filter-group">
              <label>Data</label>
              <select
                value={filters.date}
                onChange={(e) => handleFilterChange('date', e.target.value)}
                className="filter-select"
              >
                <option value="all">Qualquer data</option>
                <option value="today">Hoje</option>
                <option value="week">Esta semana</option>
                <option value="month">Este mês</option>
                <option value="year">Este ano</option>
              </select>
            </div>

            {/* Quality Filter */}
            <div className="filter-group">
              <label>Qualidade</label>
              <select
                value={filters.quality}
                onChange={(e) => handleFilterChange('quality', e.target.value)}
                className="filter-select"
              >
                <option value="all">Qualquer qualidade</option>
                <option value="360">360p</option>
                <option value="720">720p</option>
                <option value="1080">1080p</option>
                <option value="4k">4K</option>
              </select>
            </div>

            {/* Channel Filter */}
            <div className="filter-group">
              <label>Canal</label>
              <select
                value={filters.channel}
                onChange={(e) => handleFilterChange('channel', e.target.value)}
                className="filter-select"
              >
                <option value="all">Todos os canais</option>
                <option value="getv">GETV</option>
                <option value="cazetv">CAZETV</option>
                <option value="youtube">YouTube</option>
              </select>
            </div>

            {/* Reset Button */}
            <div className="filter-actions">
              <button
                type="button"
                className="reset-btn"
                onClick={resetFilters}
              >
                🔄 Limpar Filtros
              </button>
            </div>
          </div>
        )}
      </form>

      {/* Active Filters Display */}
      {Object.values(filters).some(f => f !== 'all') && (
        <div className="active-filters">
          <span className="filter-label">Filtros ativos:</span>
          {filters.type !== 'all' && (
            <span className="filter-tag">
              Tipo: {filters.type}
              <button onClick={() => handleFilterChange('type', 'all')}>✕</button>
            </span>
          )}
          {filters.duration !== 'all' && (
            <span className="filter-tag">
              Duração: {filters.duration}
              <button onClick={() => handleFilterChange('duration', 'all')}>✕</button>
            </span>
          )}
          {filters.date !== 'all' && (
            <span className="filter-tag">
              Data: {filters.date}
              <button onClick={() => handleFilterChange('date', 'all')}>✕</button>
            </span>
          )}
          {filters.quality !== 'all' && (
            <span className="filter-tag">
              Qualidade: {filters.quality}
              <button onClick={() => handleFilterChange('quality', 'all')}>✕</button>
            </span>
          )}
          {filters.channel !== 'all' && (
            <span className="filter-tag">
              Canal: {filters.channel}
              <button onClick={() => handleFilterChange('channel', 'all')}>✕</button>
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default AdvancedSearch;
