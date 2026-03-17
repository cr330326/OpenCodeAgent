import { create } from 'zustand';
import { AgentTrace, Statistics } from '../types';
import { traceApi } from '../services/api';

interface AgentInfo {
  agent_id: string;
  agent_name: string;
  status: string;
  last_seen: string;
  total_sessions: number;
  total_events: number;
}

interface OpenCodeEvent {
  event_id: string;
  agent_id: string;
  session_id?: string;
  event_category: string;
  event_type: string;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  timestamp: string;
}

interface AgentState {
  agents: AgentInfo[];
  events: OpenCodeEvent[];
  traces: AgentTrace[];
  statistics: Statistics | null;
  loading: boolean;
  error: string | null;

  fetchAgents: () => Promise<void>;
  fetchEvents: (params?: { agent_id?: string; category?: string }) => Promise<void>;
  fetchTraces: (params?: { agent_id?: string; status?: string }) => Promise<void>;
  fetchStatistics: () => Promise<void>;
  addTrace: (trace: AgentTrace) => void;
  updateTrace: (traceId: string, update: Partial<AgentTrace>) => void;
}

export const useAgentStore = create<AgentState>((set, get) => ({
  agents: [],
  events: [],
  traces: [],
  statistics: null,
  loading: false,
  error: null,

  fetchAgents: async () => {
    set({ loading: true, error: null });
    try {
      const response = await fetch('http://localhost:8000/api/v1/agents');
      const data = await response.json();
      set({ agents: data.agents || data || [], loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  fetchEvents: async (params) => {
    set({ loading: true, error: null });
    try {
      const queryParams = new URLSearchParams();
      if (params?.agent_id) queryParams.append('agent_id', params.agent_id);
      if (params?.category) queryParams.append('category', params.category);
      
      const response = await fetch(`http://localhost:8000/api/v1/events?${queryParams.toString()}`);
      const data = await response.json();
      set({ events: data.events || [], loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  fetchTraces: async (params) => {
    set({ loading: true, error: null });
    try {
      const { traces } = await traceApi.list(params);
      set({ traces, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
    }
  },

  fetchStatistics: async () => {
    try {
      const statistics = await traceApi.getStatistics();
      set({ statistics });
    } catch (error: any) {
      console.error('Failed to fetch statistics:', error);
    }
  },

  addTrace: (trace) => {
    set((state) => ({
      traces: [trace, ...state.traces].slice(0, 100),
    }));
  },

  updateTrace: (traceId, update) => {
    set((state) => ({
      traces: state.traces.map((t) =>
        t.trace_id === traceId ? { ...t, ...update } : t
      ),
    }));
  },
}));
