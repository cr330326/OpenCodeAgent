from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio

from app.config import settings
from app.storage.trace_store import TraceStore
from app.storage.event_store import EventStore
from app.hooks.tracing_hooks import TracingHooks
from app.api.traces import init_router as init_traces_router
from app.api.agents import init_router as init_agents_router
from app.api.events import init_router as init_events_router
from app.api import api_router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-Agent Visualization Platform API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trace_store: TraceStore = None
event_store: EventStore = None
hooks: TracingHooks = None


@app.on_event("startup")
async def startup_event():
    global trace_store, event_store, hooks

    logger.info("Initializing application...")

    try:
        trace_store = TraceStore(
            database_url=settings.DATABASE_URL, redis_url=settings.REDIS_URL
        )
        event_store = EventStore(
            database_url=settings.DATABASE_URL, redis_url=settings.REDIS_URL
        )

        await trace_store.init_db()
        await event_store.init_db()
        logger.info("Database initialized")

        from app.websocket_manager import ws_manager

        hooks = TracingHooks(trace_store, ws_manager)

        init_traces_router(trace_store)
        init_agents_router(hooks)
        init_events_router(event_store)

        app.include_router(api_router, prefix="/api/v1")

        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        pass


@app.on_event("shutdown")
async def shutdown_event():
    global trace_store

    logger.info("Shutting down application...")

    if trace_store:
        await trace_store.close()

    logger.info("Application shutdown complete")


@app.get("/")
async def root():
    return {
        "message": "Multi-Agent Visualization Platform",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True
    )
