import pytest
import asyncio
from datetime import datetime
import tempfile
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.storage.trace_store import TraceStore
from app.models import AgentTrace, AgentMessage, AgentStatus


@pytest.fixture
def trace_store():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    store = TraceStore(f"sqlite:///{db_path}", "")
    yield store
    os.unlink(db_path)


class TestTraceStore:
    @pytest.mark.asyncio
    async def test_save_and_get_trace(self, trace_store):
        trace = AgentTrace(
            trace_id="test-trace-1",
            session_id="session-1",
            agent_id="agent-1",
            agent_name="Test Agent",
            agent_type="worker",
            status=AgentStatus.SUCCESS,
            input_data={"query": "test"},
            started_at=datetime.now(),
        )
        await trace_store.save_trace(trace)

        result = await trace_store.get_trace("test-trace-1")
        assert result is not None
        assert result.trace_id == "test-trace-1"
        assert result.agent_id == "agent-1"

    @pytest.mark.asyncio
    async def test_get_session_traces(self, trace_store):
        for i in range(3):
            trace = AgentTrace(
                trace_id=f"trace-{i}",
                session_id="session-1",
                agent_id=f"agent-{i}",
                agent_name=f"Agent {i}",
                agent_type="worker",
                status=AgentStatus.SUCCESS,
                input_data={},
                started_at=datetime.now(),
            )
            await trace_store.save_trace(trace)

        traces = await trace_store.get_session_traces("session-1")
        assert len(traces) == 3

    @pytest.mark.asyncio
    async def test_get_all_traces(self, trace_store):
        for i in range(5):
            trace = AgentTrace(
                trace_id=f"trace-all-{i}",
                session_id=f"session-{i % 2}",
                agent_id="agent-1",
                agent_name="Agent",
                agent_type="worker",
                status=AgentStatus.SUCCESS,
                input_data={},
                started_at=datetime.now(),
            )
            await trace_store.save_trace(trace)

        traces = await trace_store.get_all_traces(limit=3)
        assert len(traces) == 3

    @pytest.mark.asyncio
    async def test_get_statistics(self, trace_store):
        for i in range(3):
            trace = AgentTrace(
                trace_id=f"trace-stat-{i}",
                session_id="session-1",
                agent_id=f"agent-{i % 2}",
                agent_name="Agent",
                agent_type="worker",
                status=AgentStatus.SUCCESS if i < 2 else AgentStatus.FAILED,
                input_data={},
                started_at=datetime.now(),
                duration_ms=100 * (i + 1),
            )
            await trace_store.save_trace(trace)

        stats = await trace_store.get_statistics()
        assert stats["total_traces"] == 3
        assert stats["total_agents"] == 2
        assert stats["success_count"] == 2
        assert stats["failed_count"] == 1

    @pytest.mark.asyncio
    async def test_save_message(self, trace_store):
        message = AgentMessage(
            message_id="msg-1",
            trace_id="trace-1",
            source_agent_id="agent-1",
            target_agent_id="agent-2",
            message_type="task",
            content={"data": "test"},
        )
        await trace_store.save_message(message)
