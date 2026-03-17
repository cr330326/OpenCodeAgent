from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime
import uuid
import time

from app.models import AgentStatus
from app.hooks import TracingHooks
from app.storage.trace_store import TraceStore
from app.storage.event_store import EventStore
from app.websocket_manager import ws_manager

router = APIRouter(tags=["agents"])

hooks: TracingHooks = None
event_store: EventStore = None


class AgentExecuteRequest(BaseModel):
    agent_id: str
    agent_name: str = "Unnamed Agent"
    agent_type: str = "worker"
    input_data: Dict[str, Any]
    session_id: str = None


class AgentExecuteResponse(BaseModel):
    trace_id: str
    agent_id: str
    status: str
    message: str


def init_router(tracing_hooks: TracingHooks, store: EventStore = None):
    global hooks, event_store
    hooks = tracing_hooks
    event_store = store


@router.get("")
async def list_agents():
    if event_store:
        agents = await event_store.get_all_agents()
        return {"agents": agents}
    return {"agents": []}


@router.post("/execute", response_model=AgentExecuteResponse)
async def execute_agent(request: AgentExecuteRequest):
    try:
        session_id = request.session_id or f"session_{uuid.uuid4().hex[:8]}"

        trace_id = await hooks.on_agent_start(
            agent_id=request.agent_id,
            input_data=request.input_data,
            session_id=session_id,
            agent_name=request.agent_name,
            agent_type=request.agent_type,
        )

        start_time = time.time()

        try:
            output_data = {"result": "Agent execution completed (demo)"}

            duration_ms = int((time.time() - start_time) * 1000)

            await hooks.on_agent_end(
                agent_id=request.agent_id,
                output_data=output_data,
                duration_ms=duration_ms,
                trace_id=trace_id,
            )

            return AgentExecuteResponse(
                trace_id=trace_id,
                agent_id=request.agent_id,
                status="success",
                message="Agent executed successfully",
            )

        except Exception as e:
            await hooks.on_agent_error(
                agent_id=request.agent_id, error=e, trace_id=trace_id
            )
            raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
