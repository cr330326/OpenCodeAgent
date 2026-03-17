import React, { useState } from 'react';
import { agentApi } from '../../services/api';
import { useAgentStore } from '../../stores/agentStore';

const AgentExecutor: React.FC = () => {
  const [agentId, setAgentId] = useState('test-agent');
  const [agentName, setAgentName] = useState('Test Agent');
  const [agentType, setAgentType] = useState('worker');
  const [inputData, setInputData] = useState('{\n  "query": "hello"\n}');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fetchTraces = useAgentStore((state) => state.fetchTraces);

  const executeAgent = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const parsedInput = JSON.parse(inputData);
      const response = await agentApi.execute({
        agent_id: agentId,
        agent_name: agentName,
        agent_type: agentType,
        input_data: parsedInput,
      });
      setResult(response);
      fetchTraces();
    } catch (err: any) {
      setError(err.message || 'Execution failed');
    } finally {
      setLoading(false);
    }
  };

  const executeBatch = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const agents = [
        { agent_id: 'research-agent', agent_name: 'Research Agent', agent_type: 'worker' },
        { agent_id: 'analysis-agent', agent_name: 'Analysis Agent', agent_type: 'worker' },
        { agent_id: 'output-agent', agent_name: 'Output Agent', agent_type: 'worker' },
      ];

      const parsedInput = JSON.parse(inputData);
      const results = [];

      for (const agent of agents) {
        const response = await agentApi.execute({
          ...agent,
          input_data: parsedInput,
        });
        results.push(response);
      }

      setResult({ batch: true, results, count: results.length });
      fetchTraces();
    } catch (err: any) {
      setError(err.message || 'Batch execution failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="agent-executor">
      <div className="form-row">
        <div className="form-group">
          <label>Agent ID:</label>
          <input
            type="text"
            value={agentId}
            onChange={(e) => setAgentId(e.target.value)}
            placeholder="test-agent"
          />
        </div>
        <div className="form-group">
          <label>Agent Name:</label>
          <input
            type="text"
            value={agentName}
            onChange={(e) => setAgentName(e.target.value)}
            placeholder="Test Agent"
          />
        </div>
        <div className="form-group">
          <label>Agent Type:</label>
          <select value={agentType} onChange={(e) => setAgentType(e.target.value)}>
            <option value="orchestrator">Orchestrator</option>
            <option value="worker">Worker</option>
            <option value="router">Router</option>
          </select>
        </div>
      </div>

      <div className="form-group">
        <label>Input Data (JSON):</label>
        <textarea
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          rows={6}
          style={{ fontFamily: 'monospace' }}
        />
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <button onClick={executeAgent} disabled={loading}>
          {loading ? 'Executing...' : 'Execute Agent'}
        </button>
        <button onClick={executeBatch} disabled={loading} style={{ background: '#722ed1' }}>
          Execute Batch (3 agents)
        </button>
      </div>

      {error && (
        <div className="error-box">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result-box">
          <h4>Result:</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      <div style={{ marginTop: 24 }}>
        <h4>Quick Test Presets:</h4>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <button
            onClick={() => setInputData('{\n  "query": "What is AI?"\n}')}
            style={{ padding: '4px 12px', fontSize: 12 }}
          >
            Simple Query
          </button>
          <button
            onClick={() =>
              setInputData(
                '{\n  "task": "analyze",\n  "data": [1, 2, 3, 4, 5],\n  "options": {"verbose": true}\n}'
              )
            }
            style={{ padding: '4px 12px', fontSize: 12 }}
          >
            Data Analysis
          </button>
          <button
            onClick={() =>
              setInputData('{\n  "action": "search",\n  "keywords": ["AI", "ML", "LLM"]\n}')
            }
            style={{ padding: '4px 12px', fontSize: 12 }}
          >
            Search Task
          </button>
        </div>
      </div>
    </div>
  );
};

export default AgentExecutor;
