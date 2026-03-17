from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class AgentOnlineStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"


class AgentStatus(BaseModel):
    agent_id: str = Field(..., description="Agent ID (项目名称)")
    agent_name: str = Field(..., description="Agent 显示名称")
    status: AgentOnlineStatus = Field(
        default=AgentOnlineStatus.OFFLINE, description="当前状态"
    )
    last_seen: Optional[datetime] = Field(None, description="最后活跃时间")
    current_session: Optional[str] = Field(None, description="当前会话ID")
    total_events: int = Field(default=0, description="总事件数")
    event_counts: Dict[str, int] = Field(
        default_factory=dict, description="按事件类型统计"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="首次发现时间"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="最后更新时间"
    )


class AgentStatusUpdate(BaseModel):
    status: Optional[AgentOnlineStatus] = None
    current_session: Optional[str] = None
    event_type: Optional[str] = None


__all__ = ["AgentOnlineStatus", "AgentStatus", "AgentStatusUpdate"]
