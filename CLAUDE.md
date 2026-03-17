# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-agent visualization platform for monitoring OpenCode plugin events:
- **Backend**: Python 3.11+ (FastAPI, Pydantic, SQLite/PostgreSQL, Redis)
- **Frontend**: React 18+ (TypeScript, ReactFlow, Zustand, dayjs)
- **Plugin**: OpenCode visualization plugin in `plugins/opencode-viz-plugin/`

## Commands

### Backend (Python)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt && pip install -r requirements-dev.txt

# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Tests
pytest                                    # All tests
pytest tests/test_trace_store.py          # Single file
pytest tests/test_trace_store.py::TestTraceStore::test_save_and_get_trace  # Single test
pytest --cov=app --cov-report=html       # With coverage

# Code quality
ruff check app/                           # Lint
ruff check app/ --fix                     # Auto-fix
black app/                                # Format
mypy app/                                 # Type check
```

### Frontend (TypeScript/React)

```bash
cd frontend

npm install
npm start                                 # Dev server (port 3000)
npm run build                             # Production build

# Tests
npm test -- --watchAll=false             # Single run
```

### Docker

```bash
docker-compose up -d --build              # Full stack
docker-compose up -d backend              # Backend only
docker-compose logs -f backend             # Follow logs
docker-compose restart backend            # Restart after changes
```

## Architecture

### Backend Structure

```
backend/app/
├── main.py              # FastAPI app, startup/shutdown, router initialization
├── config.py            # Pydantic settings
├── websocket_manager.py # WebSocket connection manager
├── api/
│   ├── agents.py        # Agent execution endpoints
│   ├── traces.py        # Trace CRUD endpoints
│   └── events.py        # OpenCode event endpoints
├── models/
│   ├── events.py        # OpenCodeEvent, EventCategory, EventType
│   └── agent_status.py  # AgentOnlineStatus, AgentStatus
├── storage/
│   ├── trace_store.py   # SQLite trace storage
│   └── event_store.py   # SQLite event storage
└── hooks/
    └── tracing_hooks.py # Agent lifecycle hooks
```

### Router Initialization Pattern

Routers use a global store that must be initialized at startup:
```python
# In main.py startup
trace_store = TraceStore(database_url=settings.DATABASE_URL)
init_traces_router(trace_store)
```

### Database

- Development: SQLite (`backend/data/agent_viz.db`)
- Production: PostgreSQL with TimescaleDB extension
- Retention: 30 days (configurable via `TRACE_RETENTION_DAYS`)

### WebSocket

Real-time updates at `/api/v1/agents/ws`

## Common Issues

1. **Backend 404 on /events**: Ensure `init_events_router(event_store)` is called in main.py startup
2. **AgentStatusInfo vs AgentStatus**: The model class is `AgentStatus`, not `AgentStatusInfo`
3. **dayjs fromNow()**: Requires `dayjs/plugin/relativeTime` to be imported and extended

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/traces` | List all traces |
| GET | `/api/v1/traces/{trace_id}` | Get trace by ID |
| GET | `/api/v1/traces/session/{session_id}` | Get traces by session |
| GET | `/api/v1/traces/statistics` | Get trace statistics |
| POST | `/api/v1/agents/execute` | Execute an agent |
| WS | `/api/v1/agents/ws` | WebSocket for real-time updates |
| GET | `/api/v1/events` | List all events |
| POST | `/api/v1/events` | Report a new event |
| GET | `/api/v1/events/statistics` | Get event statistics |
