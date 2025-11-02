import React, { useState } from 'react';
import CollectForm from './components/CollectForm';
import StatusPanel from './components/StatusPanel';
import './App.css';

function App() {
  const [taskId, setTaskId] = useState(null);
  const [showStatus, setShowStatus] = useState(false);

  const handleTaskCreated = (newTaskId) => {
    setTaskId(newTaskId);
    setShowStatus(true);
  };

  const handleCloseStatus = () => {
    setShowStatus(false);
    setTaskId(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>Flamengo AI Creator</h1>
          <p>Coleta Automatizada de Vídeos</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <CollectForm onTaskCreated={handleTaskCreated} />
          {showStatus && taskId && (
            <StatusPanel taskId={taskId} onClose={handleCloseStatus} />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 Flamengo AI Creator. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}

export default App;
