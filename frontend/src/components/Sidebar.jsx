import React, { useState } from 'react';
import '../styles/Sidebar.css';

const Sidebar = ({ activeSection, onSectionChange }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊', color: '#c22a1e' },
    { id: 'collect', label: 'Coletar Vídeos', icon: '🔍', color: '#c22a1e' },
    { id: 'downloads', label: 'Downloads', icon: '📥', color: '#c22a1e' },
    { id: 'editor', label: 'Editor de Cortes', icon: '✂️', color: '#c22a1e' },
    { id: 'templates', label: 'Templates', icon: '📋', color: '#c22a1e' },
    { id: 'analytics', label: 'Análises', icon: '📈', color: '#c22a1e' },
    { id: 'projects', label: 'Projetos', icon: '🎬', color: '#c22a1e' },
  ];

  return (
    <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="logo-container">
          <span className="logo-icon">🛡️</span>
          {!isCollapsed && <h1>Flamengo AI</h1>}
        </div>
        <button 
          className="collapse-btn"
          onClick={() => setIsCollapsed(!isCollapsed)}
          title={isCollapsed ? 'Expandir' : 'Recolher'}
        >
          {isCollapsed ? '→' : '←'}
        </button>
      </div>

      {/* Navigation Menu */}
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
            onClick={() => onSectionChange(item.id)}
            title={isCollapsed ? item.label : ''}
          >
            <span className="nav-icon">{item.icon}</span>
            {!isCollapsed && <span className="nav-label">{item.label}</span>}
          </button>
        ))}
      </nav>

      {/* Footer Info */}
      {!isCollapsed && (
        <div className="sidebar-footer">
          <p className="version">v1.0.0</p>
          <p className="status">🟢 Online</p>
        </div>
      )}
    </aside>
  );
};

export default Sidebar;
