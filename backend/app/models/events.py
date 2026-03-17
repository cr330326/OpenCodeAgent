from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class EventCategory(str, Enum):
    COMMAND = "command"
    FILE = "file"
    INSTALLATION = "installation"
    LSP = "lsp"
    MESSAGE = "message"
    PERMISSION = "permission"
    SERVER = "server"
    SESSION = "session"
    TODO = "todo"
    SHELL = "shell"
    TOOL = "tool"
    TUI = "tui"


class EventType(str, Enum):
    COMMAND_EXECUTED = "command.executed"

    FILE_EDITED = "file.edited"
    FILE_WATCHER_UPDATED = "file.watcher.updated"

    INSTALLATION_UPDATED = "installation.updated"

    LSP_CLIENT_DIAGNOSTICS = "lsp.client.diagnostics"
    LSP_UPDATED = "lsp.updated"

    MESSAGE_PART_REMOVED = "message.part.removed"
    MESSAGE_PART_UPDATED = "message.part.updated"
    MESSAGE_REMOVED = "message.removed"
    MESSAGE_UPDATED = "message.updated"

    PERMISSION_ASKED = "permission.asked"
    PERMISSION_REPLIED = "permission.replied"

    SERVER_CONNECTED = "server.connected"

    SESSION_CREATED = "session.created"
    SESSION_COMPACTED = "session.compacted"
    SESSION_DELETED = "session.deleted"
    SESSION_DIFF = "session.diff"
    SESSION_ERROR = "session.error"
    SESSION_IDLE = "session.idle"
    SESSION_STATUS = "session.status"
    SESSION_UPDATED = "session.updated"

    TODO_UPDATED = "todo.updated"

    SHELL_ENV = "shell.env"

    TOOL_EXECUTE_BEFORE = "tool.execute.before"
    TOOL_EXECUTE_AFTER = "tool.execute.after"

    TUI_PROMPT_APPEND = "tui.prompt.append"
    TUI_COMMAND_EXECUTE = "tui.command.execute"
    TUI_TOAST_SHOW = "tui.toast.show"


EVENT_CATEGORY_MAP = {
    EventType.COMMAND_EXECUTED: EventCategory.COMMAND,
    EventType.FILE_EDITED: EventCategory.FILE,
    EventType.FILE_WATCHER_UPDATED: EventCategory.FILE,
    EventType.INSTALLATION_UPDATED: EventCategory.INSTALLATION,
    EventType.LSP_CLIENT_DIAGNOSTICS: EventCategory.LSP,
    EventType.LSP_UPDATED: EventCategory.LSP,
    EventType.MESSAGE_PART_REMOVED: EventCategory.MESSAGE,
    EventType.MESSAGE_PART_UPDATED: EventCategory.MESSAGE,
    EventType.MESSAGE_REMOVED: EventCategory.MESSAGE,
    EventType.MESSAGE_UPDATED: EventCategory.MESSAGE,
    EventType.PERMISSION_ASKED: EventCategory.PERMISSION,
    EventType.PERMISSION_REPLIED: EventCategory.PERMISSION,
    EventType.SERVER_CONNECTED: EventCategory.SERVER,
    EventType.SESSION_CREATED: EventCategory.SESSION,
    EventType.SESSION_COMPACTED: EventCategory.SESSION,
    EventType.SESSION_DELETED: EventCategory.SESSION,
    EventType.SESSION_DIFF: EventCategory.SESSION,
    EventType.SESSION_ERROR: EventCategory.SESSION,
    EventType.SESSION_IDLE: EventCategory.SESSION,
    EventType.SESSION_STATUS: EventCategory.SESSION,
    EventType.SESSION_UPDATED: EventCategory.SESSION,
    EventType.TODO_UPDATED: EventCategory.TODO,
    EventType.SHELL_ENV: EventCategory.SHELL,
    EventType.TOOL_EXECUTE_BEFORE: EventCategory.TOOL,
    EventType.TOOL_EXECUTE_AFTER: EventCategory.TOOL,
    EventType.TUI_PROMPT_APPEND: EventCategory.TUI,
    EventType.TUI_COMMAND_EXECUTE: EventCategory.TUI,
    EventType.TUI_TOAST_SHOW: EventCategory.TUI,
}


class OpenCodeEvent(BaseModel):
    event_id: str = Field(..., description="事件唯一ID")
    agent_id: str = Field(..., description="Agent ID (项目名称)")
    session_id: Optional[str] = Field(None, description="会话ID")

    event_category: EventCategory = Field(..., description="事件分类")
    event_type: str = Field(..., description="事件类型")

    input_data: Dict[str, Any] = Field(default_factory=dict, description="输入数据")
    output_data: Dict[str, Any] = Field(default_factory=dict, description="输出数据")

    timestamp: datetime = Field(default_factory=datetime.now, description="事件时间")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class OpenCodeEventCreate(BaseModel):
    agent_id: str = Field(..., description="Agent ID (项目名称)")
    session_id: Optional[str] = Field(None, description="会话ID")
    event_type: str = Field(..., description="事件类型")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="输入数据")
    output_data: Dict[str, Any] = Field(default_factory=dict, description="输出数据")
    timestamp: Optional[str] = Field(None, description="事件时间 (ISO格式)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class OpenCodeEventBatch(BaseModel):
    events: List[OpenCodeEventCreate] = Field(..., description="事件列表")


class AgentStatusEnum(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"


class AgentStatusInfo(BaseModel):
    agent_id: str = Field(..., description="Agent ID")
    agent_name: str = Field(..., description="Agent 名称")
    status: AgentStatusEnum = Field(..., description="Agent 状态")
    last_seen: datetime = Field(..., description="最后活跃时间")
    current_session: Optional[str] = Field(None, description="当前会话ID")
    total_events: int = Field(0, description="总事件数")
    event_counts: Dict[str, int] = Field(
        default_factory=dict, description="各类型事件计数"
    )


class EventStatistics(BaseModel):
    total_events: int = 0
    events_by_category: Dict[str, int] = Field(default_factory=dict)
    events_by_type: Dict[str, int] = Field(default_factory=dict)
    events_by_agent: Dict[str, int] = Field(default_factory=dict)
    avg_events_per_minute: float = 0.0
