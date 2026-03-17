from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="Multi-Agent Visualization Platform",
    description="简化演示版本",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 内存存储
traces_db = {}
messages_db = []


class AgentExecuteRequest(BaseModel):
    agent_id: str
    agent_name: str = "Agent"
    agent_type: str = "worker"
    input_data: Dict[str, Any]


class AgentTrace(BaseModel):
    trace_id: str
    session_id: str
    agent_id: str
    agent_name: str
    status: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    started_at: str
    ended_at: Optional[str] = None
    duration_ms: Optional[int] = None


@app.get("/")
async def root():
    return {
        "message": "Multi-Agent Visualization Platform",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/v1/agents/execute")
async def execute_agent(request: AgentExecuteRequest):
    import time

    start = time.time()

    trace_id = f"trace_{uuid.uuid4().hex[:12]}"
    session_id = f"session_{uuid.uuid4().hex[:8]}"

    # 创建追踪记录
    trace = AgentTrace(
        trace_id=trace_id,
        session_id=session_id,
        agent_id=request.agent_id,
        agent_name=request.agent_name,
        status="running",
        input_data=request.input_data,
        started_at=datetime.now().isoformat(),
    )

    traces_db[trace_id] = trace.dict()

    # 模拟执行
    time.sleep(0.1)

    # 完成执行
    duration_ms = int((time.time() - start) * 1000)
    trace.status = "success"
    trace.output_data = {"result": f"Agent {request.agent_name} executed successfully"}
    trace.ended_at = datetime.now().isoformat()
    trace.duration_ms = duration_ms

    traces_db[trace_id] = trace.dict()

    return {
        "trace_id": trace_id,
        "agent_id": request.agent_id,
        "status": "success",
        "message": "Agent executed successfully",
        "duration_ms": duration_ms,
    }


@app.get("/api/v1/traces/session/{session_id}")
async def get_session_traces(session_id: str):
    traces = [t for t in traces_db.values() if t["session_id"] == session_id]
    return traces


@app.get("/api/v1/traces/{trace_id}")
async def get_trace(trace_id: str):
    if trace_id in traces_db:
        return traces_db[trace_id]
    return {"error": "Trace not found"}


@app.get("/api/v1/traces")
async def list_all_traces():
    return list(traces_db.values())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
