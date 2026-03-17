import React from 'react';
import FlowCanvas from './components/Canvas/FlowCanvas';
import TraceTimeline from './components/Trace/TraceTimeline';
import MonitorPanel from './components/Monitor/MonitorPanel';
import AgentExecutor from './components/Debugger/AgentExecutor';
import EventStream from './components/Events/EventStream';
import AgentList from './components/Agents/AgentList';
import { useWebSocket } from './hooks/useWebSocket';
import './App.css';

const App: React.FC = () => {
  const [selectedTab, setSelectedTab] = React.useState('canvas');
  useWebSocket();

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <h2>Agent Viz</h2>
          <span className="version">v0.2.0</span>
        </div>
        <nav className="nav">
          <button
            className={`nav-item ${selectedTab === 'canvas' ? 'active' : ''}`}
            onClick={() => setSelectedTab('canvas')}
          >
            <span className="icon">📊</span>
            Canvas
          </button>
          <button
            className={`nav-item ${selectedTab === 'timeline' ? 'active' : ''}`}
            onClick={() => setSelectedTab('timeline')}
          >
            <span className="icon">📅</span>
            Timeline
          </button>
          <button
            className={`nav-item ${selectedTab === 'monitor' ? 'active' : ''}`}
            onClick={() => setSelectedTab('monitor')}
          >
            <span className="icon">📈</span>
            Monitor
          </button>
          <button
            className={`nav-item ${selectedTab === 'events' ? 'active' : ''}`}
            onClick={() => setSelectedTab('events')}
          >
            <span className="icon">⚡</span>
            Events
          </button>
          <button
            className={`nav-item ${selectedTab === 'agents' ? 'active' : ''}`}
            onClick={() => setSelectedTab('agents')}
          >
            <span className="icon">🤖</span>
            Agents
          </button>
          <button
            className={`nav-item ${selectedTab === 'debugger' ? 'active' : ''}`}
            onClick={() => setSelectedTab('debugger')}
          >
            <span className="icon">🔧</span>
            Debugger
          </button>
        </nav>
      </aside>
      <main className="content">
        {selectedTab === 'canvas' && (
          <div className="panel">
            <h2>Agent Workflow Canvas</h2>
            <p style={{ color: '#666', marginBottom: 16 }}>
              Drag and drop to design multi-agent workflows
            </p>
            <FlowCanvas />
          </div>
        )}
        {selectedTab === 'timeline' && (
          <div className="panel">
            <h2>Execution Timeline</h2>
            <TraceTimeline />
          </div>
        )}
        {selectedTab === 'monitor' && (
          <div className="panel">
            <h2>Real-time Monitor</h2>
            <MonitorPanel />
          </div>
        )}
        {selectedTab === 'events' && (
          <div className="panel">
            <h2>Event Stream</h2>
            <EventStream />
          </div>
        )}
        {selectedTab === 'agents' && (
          <div className="panel">
            <h2>Agent Status</h2>
            <AgentList />
          </div>
        )}
        {selectedTab === 'debugger' && (
          <div className="panel">
            <h2>Agent Debugger</h2>
            <AgentExecutor />
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
