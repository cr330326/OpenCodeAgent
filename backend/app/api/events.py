from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import List, Optional, Dict, Any

from app.models.events import OpenCodeEvent, EventCategory
from app.storage.event_store import EventStore
from app.websocket_manager import ws_manager

router = APIRouter(tags=["events"])
event_store: EventStore = None


def init_router(store: EventStore):
    global event_store
    event_store = store


@router.post("")
async def report_event(event: OpenCodeEvent):
    try:
        await event_store.save_event(event)
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session_events(session_id: str):
    try:
        events = await event_store.get_events(session_id=session_id)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent/{agent_id}")
async def get_agent_events(agent_id: str):
    try:
        events = await event_store.get_events(agent_id=agent_id)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def list_agents():
    try:
        agents = await event_store.get_all_agents()
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_event_statistics():
    try:
        stats = await event_store.get_event_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
