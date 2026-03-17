import { useEffect, useRef, useCallback } from 'react';
import { useAgentStore } from '../stores/agentStore';
import { AgentTrace } from '../types';

const WS_URL = 'ws://localhost:8000/api/v1/agents/ws';

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const addTrace = useAgentStore((state) => state.addTrace);
  const updateTrace = useAgentStore((state) => state.updateTrace);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('WebSocket message:', data);

        if (data.event_type === 'agent_start' && data.data) {
          addTrace({
            trace_id: data.data.trace_id,
            session_id: data.data.session_id || '',
            agent_id: data.data.agent_id,
            agent_name: data.data.agent_id,
            agent_type: 'worker',
            status: 'running',
            input_data: {},
            started_at: data.data.timestamp || new Date().toISOString(),
            token_usage: {},
            metadata: {},
          } as AgentTrace);
        } else if (data.event_type === 'agent_end' && data.data) {
          updateTrace(data.data.trace_id, {
            status: data.data.status,
            duration_ms: data.data.duration_ms,
            ended_at: data.data.timestamp,
          });
        } else if (data.event_type === 'agent_error' && data.data) {
          updateTrace(data.data.trace_id, {
            status: 'failed',
            error_info: { error: data.data.error },
            ended_at: data.data.timestamp,
          });
        } else if (data.event_type === 'state_change' && data.data) {
          console.log(`Agent ${data.data.agent_id}: ${data.data.old_state} -> ${data.data.new_state}`);
        } else if (data.event_type === 'agent_message' && data.data) {
          console.log(`Message: ${data.data.source_agent} -> ${data.data.target_agent}`);
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected, reconnecting...');
      setTimeout(connect, 3000);
    };
  }, [addTrace, updateTrace]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return { connect, disconnect };
}
