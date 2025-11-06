import React, { useState, useEffect } from 'react';
import '../styles/DashboardStats.css';

const DashboardStats = () => {
  const [stats, setStats] = useState({
    totalDownloads: 0,
    activeProjects: 0,
    videosEdited: 0,
    totalViews: 0,
    avgEngagement: 0,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simular carregamento de dados
    // Em produção, isso viria de uma API
    setTimeout(() => {
      setStats({
        totalDownloads: 24,
        activeProjects: 5,
        videosEdited: 12,
        totalViews: 15420,
        avgEngagement: 8.5,
      });
      setLoading(false);
    }, 500);
  }, []);

  const statCards = [
    {
      id: 1,
      title: 'Total de Downloads',
      value: stats.totalDownloads,
      icon: '📥',
      color: '#c22a1e',
      trend: '+5 esta semana',
    },
    {
      id: 2,
      title: 'Projetos Ativos',
      value: stats.activeProjects,
      icon: '🎬',
      color: '#c22a1e',
      trend: '+2 novos',
    },
    {
      id: 3,
      title: 'Vídeos Editados',
      value: stats.videosEdited,
      icon: '✂️',
      color: '#c22a1e',
      trend: '+3 hoje',
    },
    {
      id: 4,
      title: 'Total de Views',
      value: stats.totalViews.toLocaleString('pt-BR'),
      icon: '👁️',
      color: '#c22a1e',
      trend: '+2.5k este mês',
    },
  ];

  return (
    <div className="dashboard-stats">
      <div className="stats-header">
        <h2>📊 Dashboard</h2>
        <p className="subtitle">Visão geral do seu desempenho</p>
      </div>

      {loading ? (
        <div className="loading">Carregando estatísticas...</div>
      ) : (
        <div className="stats-grid">
          {statCards.map((card) => (
            <div key={card.id} className="stat-card">
              <div className="card-header">
                <span className="card-icon">{card.icon}</span>
                <span className="card-title">{card.title}</span>
              </div>
              <div className="card-value">{card.value}</div>
              <div className="card-trend">{card.trend}</div>
            </div>
          ))}
        </div>
      )}

      {/* Activity Chart */}
      <div className="activity-section">
        <h3>📈 Atividade Recente</h3>
        <div className="activity-chart">
          <div className="chart-bar" style={{ height: '60%' }}>
            <span>Seg</span>
          </div>
          <div className="chart-bar" style={{ height: '75%' }}>
            <span>Ter</span>
          </div>
          <div className="chart-bar" style={{ height: '45%' }}>
            <span>Qua</span>
          </div>
          <div className="chart-bar" style={{ height: '85%' }}>
            <span>Qui</span>
          </div>
          <div className="chart-bar" style={{ height: '70%' }}>
            <span>Sex</span>
          </div>
          <div className="chart-bar" style={{ height: '90%' }}>
            <span>Sab</span>
          </div>
          <div className="chart-bar" style={{ height: '55%' }}>
            <span>Dom</span>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h3>⚡ Ações Rápidas</h3>
        <div className="actions-grid">
          <button className="action-btn">
            <span className="action-icon">🔍</span>
            <span>Buscar Vídeos</span>
          </button>
          <button className="action-btn">
            <span className="action-icon">📥</span>
            <span>Novo Download</span>
          </button>
          <button className="action-btn">
            <span className="action-icon">✂️</span>
            <span>Editar Corte</span>
          </button>
          <button className="action-btn">
            <span className="action-icon">📋</span>
            <span>Novo Projeto</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardStats;
