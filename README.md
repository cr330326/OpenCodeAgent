# Multi-Agent Visualization Platform

A real-time visualization platform for monitoring OpenCode plugin events and multi-agent systems.

## Features

- **Real-time Monitoring**: Track agent events, traces, and messages in real-time via WebSocket
- **Visual Workflow**: Interactive canvas with ReactFlow for agent workflow visualization
- **Event Stream**: Monitor all 25+ OpenCode event types (command, file, LSP, message, permission, server, session, todo, shell, tool, TUI)
- **Trace Timeline**: View agent execution traces with timing and status information
- **Statistics Dashboard**: Monitor system health and performance metrics
- **Agent Management**: Track multiple agents with online/offline status

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, FastAPI, Pydantic |
| Frontend | React 18, TypeScript, ReactFlow, Zustand, dayjs |
| Database | SQLite (dev), PostgreSQL/TimescaleDB (prod) |
| Cache | Redis |
| Deployment | Docker, Docker Compose |

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/cr330326/OpenCodeAgent.git
cd OpenCodeAgent

# Start all services
docker-compose up -d --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## Project Structure

```
OpenCodeAgent/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routes
│   │   │   ├── agents.py     # Agent execution endpoints
│   │   │   ├── events.py     # OpenCode event endpoints
│   │   │   └── traces.py     # Trace CRUD endpoints
│   │   ├── models/           # Pydantic data models
│   │   │   ├── events.py     # OpenCodeEvent, EventCategory, EventType
│   │   │   └── agent_status.py
│   │   ├── storage/          # Database layer
│   │   │   ├── trace_store.py
│   │   │   └── event_store.py
│   │   ├── hooks/            # Agent lifecycle hooks
│   │   ├── main.py           # FastAPI application
│   │   └── config.py         # Configuration settings
│   ├── tests/                # Test files
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Canvas/       # ReactFlow visualization
│   │   │   ├── Trace/        # Trace timeline
│   │   │   ├── Monitor/      # Statistics panel
│   │   │   ├── Events/       # Event stream
│   │   │   ├── Agents/       # Agent list
│   │   │   └── Debugger/     # Agent executor
│   │   ├── stores/           # Zustand state management
│   │   ├── services/         # API client
│   │   └── types/            # TypeScript interfaces
│   └── package.json
├── plugins/
│   └── opencode-viz-plugin/  # OpenCode integration plugin
├── docker-compose.yml
└── AGENTS.md                 # Development guidelines
```

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

## Event Categories

The platform monitors the following OpenCode event categories:

- **Command Events**: Command execution and lifecycle
- **File Events**: File read, write, edit operations
- **LSP Events**: Language server protocol interactions
- **Message Events**: Agent communication messages
- **Permission Events**: Permission requests and grants
- **Server Events**: Server lifecycle and health
- **Session Events**: Session start, end, and management
- **Todo Events**: Task and todo list updates
- **Shell Events**: Shell command execution
- **Tool Events**: Tool invocations and results
- **TUI Events**: Terminal UI interactions

## Development

### Running Tests

**Backend:**
```bash
cd backend
pytest                                    # All tests
pytest tests/test_trace_store.py          # Single file
pytest --cov=app --cov-report=html        # With coverage
```

**Frontend:**
```bash
cd frontend
npm test                                  # All tests
npm test -- --watchAll=false              # Single run
```

### Code Quality

```bash
# Backend
ruff check app/                           # Lint
black app/                                # Format
mypy app/                                 # Type check

# Frontend
npm run build                             # Build check
```

## Configuration

Environment variables can be set in `backend/.env`:

```env
DATABASE_URL=sqlite:///./data/agent_viz.db
REDIS_URL=redis://localhost:6379/0
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:3000"]
TRACE_RETENTION_DAYS=30
```

## Data Retention

- Default retention period: **30 days**
- Configurable via `TRACE_RETENTION_DAYS` environment variable
- Automatic cleanup of old events and traces

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [ReactFlow](https://reactflow.dev/) - Interactive node-based graphs
- [Zustand](https://github.com/pmndrs/zustand) - Lightweight state management
- [OpenCode](https://opencode.ai) - AI coding assistant platform
