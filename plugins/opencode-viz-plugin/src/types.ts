export type EventType = 
  // Command events
  COMMAND_EXECUTED = "command.executed"
  
  // File events
  FILE_EDITED = "file.edited"
  FILE_WATCHER_UPDATED = "file.watcher.updated"
  
  // Installation events
  INSTALLATION_UPDATED = "installation.updated"
  
  // LSP events
  LSP_CLIENT_DIAGNOSTICS = "lsp.client.diagnostics"
  LSP_UPDATED = "lsp.updated"
  
  // Message events
  MESSAGE_PART_REMOVED = "message.part.removed"
  MESSAGE_PART_UPDATED = "message.part.updated"
  MESSAGE_REMOVED = "message.removed"
  MESSAGE_UPDATED = "message.updated"
  
  // Permission events
  PERMISSION_ASKED = "permission.asked"
  PERMISSION_REPLIED = "permission.replied"
  
  // Server events
  SERVER_CONNECTED = "server.connected"
  
  // Session events
  SESSION_CREATED = "session.created"
  SESSION_COMPACTED = "session.compacted"
    SESSION_DELETED = "session.deleted"
    SESSION_DIFF = "session.diff"
    SESSION_ERROR = "session.error"
    SESSION_IDLE = "session.idle"
    SESSION_STATUS = "session.status"
    SESSION_UPDATED = "session.updated"
    
    // Todo events
    TODO_UPDATED = "todo.updated"
    
    // Shell events
    SHELL_ENV = "shell.env"
    
    // Tool events
    TOOL_EXECUTE_BEFORE = "tool.execute.before"
    TOOL_EXECUTE_AFTER = "tool.execute.after"
    
    // TUI events
    TUI_PROMPT_APPEND = "tui.prompt.append"
    TUI_COMMAND_EXECUTE = "tui.command.execute"
    TUI_TOAST_SHOW = "tui.toast.show"

`

export const EVENT_TYPE_MAP: Record<EventType, string> = {
    const event_type: EventType;
    return event
});

