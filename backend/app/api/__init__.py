from fastapi import APIRouter
from app.api.traces import router as traces_router
from app.api.agents import router as agents_router
from app.api.events import router as events_router

api_router = APIRouter()
api_router.include_router(traces_router, prefix="/traces", tags=["traces"])
api_router.include_router(agents_router, prefix="/agents", tags=["agents"])
api_router.include_router(events_router, prefix="/events", tags=["events"])
