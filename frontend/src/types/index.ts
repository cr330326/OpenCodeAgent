export interface AgentTrace {
  trace_id: string;
  session_id: string;
  parent_trace_id?: string;
  agent_id: string;
  agent_name: string;
  agent_type: string;
  status: 'idle' | 'pending' | 'running' | 'success' | 'failed' | 'retrying';
  input_data: Record<string, any>;
  output_data?: Record<string, any>;
  error_info?: Record<string, any>;
  started_at: string;
  ended_at?: string;
  duration_ms?: number;
  token_usage: Record<string, number>;
  metadata: Record<string, any>;
}

export interface AgentMetrics {
  agent_id: string;
  time_window: string;
  total_executions: number;
  success_count: number;
  failed_count: number;
  avg_duration_ms: number;
  success_rate: number;
  error_rate: number;
}

export interface Statistics {
  total_traces: number;
  total_agents: number;
  total_sessions: number;
  success_count: number;
  failed_count: number;
  avg_duration_ms: number;
}

export interface OpenCodeEvent {
  event_id: string;
  agent_id: string;
  session_id?: string;
  event_category: string;
  event_type: string;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  timestamp: string;
}

export interface AgentInfo {
  agent_id: string;
  agent_name: string;
  status: string;
  last_seen: string;
  total_sessions: number;
  total_events: number;
}
