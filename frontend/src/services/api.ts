import axios from 'axios';
import { AgentTrace, Statistics } from '../types';

const API_BASE = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

export const agentApi = {
  execute: async (data: {
    agent_id: string;
    agent_name?: string;
    agent_type?: string;
    input_data: Record<string, any>;
    session_id?: string;
  }): Promise<{ trace_id: string; status: string }> => {
    const response = await api.post('/agents/execute', {
      agent_name: 'Agent',
      agent_type: 'worker',
      ...data,
    });
    return response.data;
  },
};

export const traceApi = {
  list: async (params?: {
    limit?: number;
    offset?: number;
    agent_id?: string;
    status?: string;
  }): Promise<{ traces: AgentTrace[] }> => {
    const response = await api.get('/traces', { params });
    return response.data;
  },

  get: async (traceId: string): Promise<AgentTrace> => {
    const response = await api.get(`/traces/${traceId}`);
    return response.data;
  },

  getSession: async (sessionId: string): Promise<AgentTrace[]> => {
    const response = await api.get(`/traces/session/${sessionId}`);
    return response.data;
  },

  getMetrics: async (agentId: string, timeWindow = '24h'): Promise<any> => {
    const response = await api.get(`/traces/metrics/${agentId}`, {
      params: { time_window: timeWindow },
    });
    return response.data;
  },

  getStatistics: async (): Promise<Statistics> => {
    const response = await api.get('/traces/statistics');
    return response.data;
  },
};

export const eventApi = {
  list: async (params?: {
    agent_id?: string;
    category?: string;
    event_type?: string;
    limit?: number;
  }): Promise<{ events: any[] }> => {
    const response = await api.get('/events', { params });
    return response.data;
  },

  report: async (event: {
    agent_id: string;
    event_type: string;
    input_data?: Record<string, any>;
    output_data?: Record<string, any>;
    session_id?: string;
  }): Promise<any> => {
    const response = await api.post('/events', event);
    return response.data;
  },
};

export const agentsApi = {
  list: async (): Promise<{ agents: any[] }> => {
    const response = await api.get('/agents');
    return response.data;
  },

  get: async (agentId: string): Promise<any> => {
    const response = await api.get(`/agents/${agentId}`);
    return response.data;
  },
};
