from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum

from app.models.events import (
    OpenCodeEvent,
    EventCategory,
    EventType,
    EVENT_CATEGORY_MAP,
)
from app.models.agent_status import AgentOnlineStatus, AgentStatus


class TraceStatus(str, Enum):
    IDLE = "idle"
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


class TraceLevel(str, Enum):
    INFO = "info"
    warning = "warning"
    error = "error"
    debug = "debug"


class AgentTrace(BaseModel):
    trace_id: str = Field(..., description="唯一追踪ID")
    session_id: str = Field(..., description="会话ID")
    parent_trace_id: Optional[str] = Field(None, description="父追踪ID")

    agent_id: str = Field(..., description="Agent ID")
    agent_name: str = Field(..., description="Agent名称")
    agent_type: str = Field(..., description="Agent类型")

    status: TraceStatus = Field(..., description="执行状态")

    input_data: Dict[str, Any] = Field(default_factory=dict, description="输入数据")
    output_data: Optional[Dict[str, Any]] = Field(None, description="输出数据")
    error_info: Optional[Dict[str, Any]] = Field(None, description="错误信息")

    started_at: datetime = Field(..., description="开始时间")
    ended_at: Optional[datetime] = Field(None, description="结束时间")
    duration_ms: Optional[int] = Field(None, description="执行耗时(毫秒)")

    token_usage: Dict[str, int] = Field(default_factory=dict, description="Token消耗")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class AgentMessage(BaseModel):
    message_id: str = Field(..., description="消息ID")
    trace_id: str = Field(..., description="关联的trace ID")

    source_agent_id: str = Field(..., description="发送方Agent ID")
    target_agent_id: str = Field(..., description="接收方Agent ID")

    message_type: str = Field(..., description="消息类型")
    content: Any = Field(..., description="消息内容")

    timestamp: datetime = Field(default_factory=datetime.now)


class WorktreeNode(BaseModel):
    agent_id: str
    agent_name: str
    agent_type: str
    status: TraceStatus

    local_context: Dict[str, Any] = Field(default_factory=dict)
    shared_memory_keys: List[str] = Field(default_factory=list)

    children: List["WorktreeNode"] = Field(default_factory=list)
    traces: List[str] = Field(default_factory=list)


class WorkflowDefinition(BaseModel):
    workflow_id: str
    name: str
    description: str

    nodes: List[Dict[str, Any]] = Field(..., description="节点定义")
    edges: List[Dict[str, Any]] = Field(..., description="边定义")

    variables: Dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AgentMetrics(BaseModel):
    agent_id: str
    time_window: str = Field(..., description="时间窗口")

    total_executions: int = 0
    success_count: int = 0
    failed_count: int = 0

    avg_duration_ms: float = 0.0
    p50_duration_ms: float = 0.0
    p95_duration_ms: float = 0.0
    p99_duration_ms: float = 0.0

    total_tokens: int = 0
    avg_tokens_per_execution: float = 0.0

    success_rate: float = Field(0.0, ge=0, le=1)
    error_rate: float = Field(0.0, ge=0, le=1)


__all__ = [
    "TraceStatus",
    "TraceLevel",
    "AgentTrace",
    "AgentMessage",
    "WorktreeNode",
    "WorkflowDefinition",
    "AgentMetrics",
    "OpenCodeEvent",
    "EventCategory",
    "EventType",
    "EVENT_CATEGORY_MAP",
    "AgentOnlineStatus",
    "AgentStatus",
]
