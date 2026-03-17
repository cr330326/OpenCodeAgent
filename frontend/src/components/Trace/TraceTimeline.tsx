import React, { useEffect, useState } from 'react';
import { useAgentStore } from '../../stores/agentStore';
import dayjs from 'dayjs';

const statusColors: Record<string, string> = {
  idle: '#d9d9d9',
  pending: '#faad14',
  running: '#1890ff',
  success: '#52c41a',
  failed: '#ff4d4f',
  retrying: '#fa8c16',
};

const TraceTimeline: React.FC = () => {
  const { traces, loading, error, fetchTraces } = useAgentStore();
  const [filter, setFilter] = useState({
    agent_id: '',
    status: '',
  });

  useEffect(() => {
    fetchTraces();
  }, [fetchTraces]);

  const handleFilter = () => {
    fetchTraces(filter);
  };

  const handleClearFilter = () => {
    setFilter({ agent_id: '', status: '' });
    fetchTraces();
  };

  if (loading) {
    return <div style={{ padding: 20 }}>Loading traces...</div>;
  }

  if (error) {
    return (
      <div style={{ padding: 20, color: '#ff4d4f' }}>
        Error: {error}
        <button onClick={() => fetchTraces()} style={{ marginLeft: 16 }}>
          Retry
        </button>
      </div>
    );
  }

  if (traces.length === 0) {
    return (
      <div style={{ padding: 20, color: '#666' }}>
        No traces found. Execute an agent to see traces.
      </div>
    );
  }

  return (
    <div className="trace-timeline">
      <div className="filter-bar">
        <input
          type="text"
          placeholder="Filter by Agent ID"
          value={filter.agent_id}
          onChange={(e) => setFilter({ ...filter, agent_id: e.target.value })}
        />
        <select
          value={filter.status}
          onChange={(e) => setFilter({ ...filter, status: e.target.value })}
        >
          <option value="">All Status</option>
          <option value="success">Success</option>
          <option value="failed">Failed</option>
          <option value="running">Running</option>
        </select>
        <button onClick={handleFilter}>Filter</button>
        <button onClick={handleClearFilter} style={{ background: '#666' }}>
          Clear
        </button>
        <span style={{ color: '#666', marginLeft: 16 }}>{traces.length} traces</span>
      </div>

      <div className="trace-list">
        {traces.map((trace) => (
          <div
            key={trace.trace_id}
            className="trace-card"
            style={{
              borderLeftColor: statusColors[trace.status] || '#d9d9d9',
            }}
          >
            <div className="trace-header">
              <strong>{trace.agent_name || trace.agent_id}</strong>
              <span
                className="status-badge"
                style={{
                  background: statusColors[trace.status] || '#d9d9d9',
                }}
              >
                {trace.status}
              </span>
            </div>
            <div className="trace-meta">
              <div>Session: {trace.session_id}</div>
              <div>Started: {dayjs(trace.started_at).format('YYYY-MM-DD HH:mm:ss')}</div>
              {trace.duration_ms !== undefined && trace.duration_ms > 0 && (
                <div>Duration: {trace.duration_ms}ms</div>
              )}
            </div>
            {trace.input_data && Object.keys(trace.input_data).length > 0 && (
              <details className="trace-details">
                <summary>Input Data</summary>
                <pre>{JSON.stringify(trace.input_data, null, 2)}</pre>
              </details>
            )}
            {trace.output_data && (
              <details className="trace-details">
                <summary>Output Data</summary>
                <pre>{JSON.stringify(trace.output_data, null, 2)}</pre>
              </details>
            )}
            {trace.error_info && (
              <div className="error-box">
                <strong>Error:</strong> {JSON.stringify(trace.error_info)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TraceTimeline;
