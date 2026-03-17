import React, { useEffect, useState } from 'react';
import { useAgentStore } from '../../stores/agentStore';

const MonitorPanel: React.FC = () => {
  const { statistics, fetchStatistics } = useAgentStore();
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    fetchStatistics();
    let interval: NodeJS.Timeout;
    if (autoRefresh) {
      interval = setInterval(fetchStatistics, 5000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [fetchStatistics, autoRefresh]);

  if (!statistics) {
    return <div style={{ padding: 20 }}>Loading statistics...</div>;
  }

  const successRate =
    statistics.total_traces > 0
      ? ((statistics.success_count / statistics.total_traces) * 100).toFixed(1)
      : '0';

  return (
    <div className="monitor-panel">
      <div style={{ marginBottom: 16, display: 'flex', gap: 16, alignItems: 'center' }}>
        <button onClick={() => fetchStatistics()}>Refresh</button>
        <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={(e) => setAutoRefresh(e.target.checked)}
          />
          Auto-refresh (5s)
        </label>
      </div>

      <div className="stat-grid">
        <div className="stat-card" style={{ borderLeftColor: '#1890ff' }}>
          <div className="label">Total Traces</div>
          <div className="value" style={{ color: '#1890ff' }}>
            {statistics.total_traces}
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#722ed1' }}>
          <div className="label">Total Agents</div>
          <div className="value" style={{ color: '#722ed1' }}>
            {statistics.total_agents}
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#13c2c2' }}>
          <div className="label">Total Sessions</div>
          <div className="value" style={{ color: '#13c2c2' }}>
            {statistics.total_sessions}
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#52c41a' }}>
          <div className="label">Success Rate</div>
          <div className="value" style={{ color: '#52c41a' }}>
            {successRate}%
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#52c41a' }}>
          <div className="label">Success Count</div>
          <div className="value" style={{ color: '#52c41a' }}>
            {statistics.success_count}
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#ff4d4f' }}>
          <div className="label">Failed Count</div>
          <div className="value" style={{ color: '#ff4d4f' }}>
            {statistics.failed_count}
          </div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#fa8c16' }}>
          <div className="label">Avg Duration</div>
          <div className="value" style={{ color: '#fa8c16' }}>
            {statistics.avg_duration_ms.toFixed(2)}ms
          </div>
        </div>
      </div>

      <div style={{ marginTop: 24 }}>
        <h3>System Status</h3>
        <div
          style={{
            display: 'flex',
            gap: 24,
            marginTop: 12,
            padding: 16,
            background: '#fafafa',
            borderRadius: 8,
          }}
        >
          <StatusIndicator label="Backend API" status="online" />
          <StatusIndicator label="WebSocket" status="online" />
          <StatusIndicator label="Database" status="online" />
        </div>
      </div>

      <div style={{ marginTop: 24 }}>
        <h3>Quick Actions</h3>
        <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
          <button
            onClick={async () => {
              const res = await fetch('http://localhost:8000/api/v1/traces/cleanup?days=7', {
                method: 'POST',
              });
              const data = await res.json();
              alert(`Cleanup: ${data.traces_deleted} traces deleted`);
              fetchStatistics();
            }}
            style={{ background: '#ff4d4f' }}
          >
            Cleanup Old Data (7 days)
          </button>
        </div>
      </div>
    </div>
  );
};

const StatusIndicator: React.FC<{ label: string; status: 'online' | 'offline' }> = ({
  label,
  status,
}) => (
  <div className="status-indicator">
    <div className={`status-dot ${status}`} />
    <span>{label}</span>
  </div>
);

export default MonitorPanel;
