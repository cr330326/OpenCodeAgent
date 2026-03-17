import React, { useEffect, useState } from 'react';
import { useAgentStore } from '../../stores/agentStore';
import dayjs from 'dayjs';

const statusColors: Record<string, string> = {
  command: '#722ed1',
  file: '#faad14',
  installation: '#faad14',
  lsp: '#fa8c16',
  message: '#1890ff',
  permission: '#ff4d4f',
  server: '#52c41a',
  session: '#faad14',
  shell: '#13c2c2',
  tool: '#1890ff',
  tui: '#722ed1',
};

const categoryLabels: Record<string, string> = {
  command: 'Command',
  file: 'File',
  installation: 'Installation',
  lsp: 'LSP',
  message: 'Message',
  permission: 'Permission',
  server: 'Server',
  session: 'Session',
  todo: 'Todo',
  shell: 'Shell',
  tool: 'Tool',
  tui: 'TUI',
};

const EventStream: React.FC = () => {
  const { events, loading, error, fetchEvents } = useAgentStore();
  const [filter, setFilter] = useState({ category: '', eventType: '' });
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    fetchEvents();
  }, [fetchEvents]);

  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      fetchEvents();
    }, 5000);
    return () => clearInterval(interval);
  }, [autoRefresh, fetchEvents]);

  const handleFilter = () => {
    fetchEvents(filter);
  };

  const handleClearFilter = () => {
    setFilter({ category: '', eventType: '' });
    fetchEvents();
  };

  if (loading) {
    return <div style={{ padding: 20 }}>Loading events...</div>;
  }

  if (error) {
    return (
      <div style={{ padding: 20, color: '#ff4d4f' }}>
        Error: {error}
        <button onClick={handleClearFilter} style={{ marginLeft: 16 }}>
          Retry
        </button>
      </div>
    );
  }

  if (!events || events.length === 0) {
    return (
      <div style={{ padding: 40, textAlign: 'center', color: '#666' }}>
        No events found. Execute an agent to see events.
      </div>
    );
  }

  return (
    <div className="event-stream">
      <div className="event-filters">
        <select
          value={filter.category}
          onChange={(e) => setFilter({ ...filter, category: e.target.value })}
        >
          <option value="">All Categories</option>
          {Object.keys(categoryLabels).map((key) => (
            <option key={key} value={key}>
              {categoryLabels[key]}
            </option>
          ))}
        </select>
        <button onClick={handleFilter}>Filter</button>
        <button onClick={handleClearFilter} style={{ background: '#666', marginLeft: 8 }}>
          Clear
        </button>
        <label style={{ marginLeft: 16 }}>
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={(e) => setAutoRefresh(e.target.checked)}
          />
          Auto-refresh (5s)
        </label>
        <span style={{ marginLeft: 16, color: '#666' }}>
          {events.length} events
        </span>
      </div>

      <div className="event-list">
        {events.map((event: any) => (
          <div
            key={event.event_id}
            className="event-card"
            style={{
              borderLeftColor: statusColors[event.event_category] || '#d9d9d9',
            }}
          >
            <div className="event-header">
              <span className="event-category">
                {categoryLabels[event.event_category] || event.event_category}
              </span>
              <span className="event-type">{event.event_type}</span>
              <span className="event-time">
                {dayjs(event.timestamp).format('HH:mm:ss')}
              </span>
            </div>
            <div className="event-meta">
              <div>Agent: {event.agent_id}</div>
              <div>Session: {event.session_id || '-'}</div>
            </div>
            {event.input_data && Object.keys(event.input_data).length > 0 && (
              <details className="event-details">
                <summary>Input Data</summary>
                <pre style={{ fontSize: 11, margin: 0, padding: 12, background: '#282c34', color: '#abb2bf', overflowX: 'auto' }}>
                  {JSON.stringify(event.input_data, null, 2)}
                </pre>
              </details>
            )}
            {event.output_data && Object.keys(event.output_data).length > 0 && (
              <details className="event-details">
                <summary>Output Data</summary>
                <pre style={{ fontSize: 11, margin: 0, padding: 12, background: '#282c34', color: '#abb2bf', overflowX: 'auto' }}>
                  {JSON.stringify(event.output_data, null, 2)}
                </pre>
              </details>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventStream;
