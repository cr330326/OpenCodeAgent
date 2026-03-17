import pytest
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import AgentTrace, AgentMessage, AgentStatus


class TestModels:
    def test_agent_trace_creation(self):
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
        assert trace.trace_id == "test-trace-1"
        assert trace.agent_id == "agent-1"
        assert trace.status == AgentStatus.SUCCESS
        assert trace.input_data == {"query": "test"}

    def test_agent_trace_with_output(self):
        trace = AgentTrace(
            trace_id="test-trace-2",
            session_id="session-1",
            agent_id="agent-1",
            agent_name="Test Agent",
            agent_type="worker",
            status=AgentStatus.SUCCESS,
            input_data={"query": "test"},
            output_data={"result": "success"},
            started_at=datetime.now(),
            ended_at=datetime.now(),
            duration_ms=100,
        )
        assert trace.output_data == {"result": "success"}
        assert trace.duration_ms == 100

    def test_agent_message_creation(self):
        message = AgentMessage(
            message_id="msg-1",
            trace_id="trace-1",
            source_agent_id="agent-1",
            target_agent_id="agent-2",
            message_type="task",
            content={"data": "test"},
        )
        assert message.message_id == "msg-1"
        assert message.source_agent_id == "agent-1"
        assert message.target_agent_id == "agent-2"
