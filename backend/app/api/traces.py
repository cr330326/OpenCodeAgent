from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from app.models import AgentTrace, AgentMetrics
from app.storage.trace_store import TraceStore

router = APIRouter(tags=["traces"])

trace_store: TraceStore = None


def init_router(store: TraceStore):
    global trace_store
    trace_store = store


@router.get("")
async def list_traces(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    agent_id: Optional[str] = None,
    status: Optional[str] = None,
):
    try:
        traces = await trace_store.get_all_traces(
            limit=limit, offset=offset, agent_id=agent_id, status=status
        )
        return {"traces": traces, "limit": limit, "offset": offset}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics():
    try:
        stats = await trace_store.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}", response_model=List[AgentTrace])
async def get_session_traces(session_id: str):
    try:
        traces = await trace_store.get_session_traces(session_id)
        return traces
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{trace_id}", response_model=AgentTrace)
async def get_trace(trace_id: str):
    trace = await trace_store.get_trace(trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    return trace


@router.get("/metrics/{agent_id}", response_model=AgentMetrics)
async def get_agent_metrics(agent_id: str, time_window: str = "24h"):
    try:
        metrics = await trace_store.get_agent_metrics(agent_id, time_window)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup")
async def cleanup_old_traces(days: int = 30):
    try:
        result = await trace_store.cleanup_old_data(days)
        return {
            "message": f"Cleaned up data older than {days} days",
            **result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
