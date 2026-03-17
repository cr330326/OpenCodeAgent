import React, { useEffect, useState } from 'react';
import { useAgentStore } from '../../stores/agentStore';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

const statusColors: Record<string, string> = {
  online: '#52c41a',
  offline: '#ff4d4f',
  busy: '#1890ff',
  idle: '#faad14',
  error: '#ff4d4f',
};

const AgentList: React.FC = () => {
  const { agents, loading, error, fetchAgents } = useAgentStore();
  const [selectedAgent, setSelectedAgent] = useState<any>(null);

  useEffect(() => {
    fetchAgents();
  }, [fetchAgents]);

  if (loading) {
    return <div style={{ padding: 20 }}>Loading agents...</div>;
  }

  if (error) {
    return (
      <div style={{ padding: 20, color: '#ff4d4f' }}>
        Error: {error}
        <button onClick={() => fetchAgents()} style={{ marginLeft: 16 }}>
          Retry
        </button>
      </div>
    );
  }

  if (!agents || agents.length === 0) {
    return (
      <div style={{ padding: 20, color: '#666' }}>
        No agents found. Register an agent first.
      </div>
    );
  }

  return (
    <div className="agent-list">
      {agents.map((agent: any) => (
        <div
          key={agent.agent_id}
          className="agent-card"
          style={{
            borderLeftColor: statusColors[agent.status] || '#d9d9d9',
          }}
          onClick={() => setSelectedAgent(selectedAgent?.agent_id === agent.agent_id ? null : agent)}
        >
          <div className="agent-header">
            <span className="agent-name">{agent.agent_name || agent.agent_id}</span>
            <span
              className="status-badge"
              style={{ background: statusColors[agent.status] || '#d9d9d9' }}
            >
              {agent.status}
            </span>
          </div>
          <div className="agent-meta">
            <div>Sessions: {agent.total_sessions || 0}</div>
            <div>Last seen: {agent.last_seen ? dayjs(agent.last_seen).fromNow() : 'N/A'}</div>
            <div className="agent-stats">
              <span>Events: {agent.total_events || 0}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default AgentList;
