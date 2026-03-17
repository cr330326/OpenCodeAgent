from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import uuid
import asyncio
import logging

from app.models import AgentTrace, AgentStatus, AgentMessage
from app.storage.trace_store import TraceStore

logger = logging.getLogger(__name__)


class AgentHooks(ABC):
    @abstractmethod
    async def on_agent_start(self, agent_id: str, input_data: Dict[str, Any], **kwargs):
        pass

    @abstractmethod
    async def on_agent_end(
        self, agent_id: str, output_data: Dict[str, Any], duration_ms: int, **kwargs
    ):
        pass

    @abstractmethod
    async def on_agent_error(self, agent_id: str, error: Exception, **kwargs):
        pass

    @abstractmethod
    async def on_llm_start(self, agent_id: str, prompt: str, **kwargs):
        pass

    @abstractmethod
    async def on_llm_end(
        self, agent_id: str, response: str, token_usage: Dict[str, int], **kwargs
    ):
        pass

    @abstractmethod
    async def on_tool_start(
        self, agent_id: str, tool_name: str, params: Dict[str, Any], **kwargs
    ):
        pass

    @abstractmethod
    async def on_tool_end(self, agent_id: str, tool_name: str, result: Any, **kwargs):
        pass

    @abstractmethod
    async def on_state_change(
        self, agent_id: str, old_state: str, new_state: str, **kwargs
    ):
        pass

    @abstractmethod
    async def on_message_send(
        self, source_agent: str, target_agent: str, message: Any, **kwargs
    ):
        pass


class TracingHooks(AgentHooks):
    def __init__(self, trace_store: TraceStore, websocket_manager=None):
        self.trace_store = trace_store
        self.websocket_manager = websocket_manager
        self.active_traces: Dict[str, AgentTrace] = {}

    async def on_agent_start(self, agent_id: str, input_data: Dict[str, Any], **kwargs):
        trace_id = f"trace_{uuid.uuid4().hex[:12]}"
        session_id = kwargs.get("session_id", f"session_{uuid.uuid4().hex[:8]}")

        trace = AgentTrace(
            trace_id=trace_id,
            session_id=session_id,
            parent_trace_id=kwargs.get("parent_trace_id"),
            agent_id=agent_id,
            agent_name=kwargs.get("agent_name", agent_id),
            agent_type=kwargs.get("agent_type", "worker"),
            status=AgentStatus.RUNNING,
            input_data=input_data,
            started_at=datetime.now(),
            metadata=kwargs.get("metadata", {}),
        )

        self.active_traces[trace_id] = trace
        await self.trace_store.save_trace(trace)

        await self._push_to_frontend(
            "agent_start",
            {
                "trace_id": trace_id,
                "agent_id": agent_id,
                "status": "running",
                "timestamp": datetime.now().isoformat(),
            },
        )

        logger.info(f"Agent started: {agent_id} (trace: {trace_id})")
        return trace_id

    async def on_agent_end(
        self, agent_id: str, output_data: Dict[str, Any], duration_ms: int, **kwargs
    ):
        trace_id = kwargs.get("trace_id")
        if not trace_id or trace_id not in self.active_traces:
            logger.warning(f"Trace not found: {trace_id}")
            return

        trace = self.active_traces[trace_id]
        trace.output_data = output_data
        trace.status = AgentStatus.SUCCESS
        trace.ended_at = datetime.now()
        trace.duration_ms = duration_ms

        await self.trace_store.save_trace(trace)

        await self._push_to_frontend(
            "agent_end",
            {
                "trace_id": trace_id,
                "agent_id": agent_id,
                "status": "success",
                "duration_ms": duration_ms,
                "timestamp": datetime.now().isoformat(),
            },
        )

        logger.info(f"Agent completed: {agent_id} (duration: {duration_ms}ms)")
        del self.active_traces[trace_id]

    async def on_agent_error(self, agent_id: str, error: Exception, **kwargs):
        trace_id = kwargs.get("trace_id")
        if not trace_id or trace_id not in self.active_traces:
            logger.warning(f"Trace not found: {trace_id}")
            return

        trace = self.active_traces[trace_id]
        trace.status = AgentStatus.FAILED
        trace.ended_at = datetime.now()
        trace.error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
        }

        await self.trace_store.save_trace(trace)

        await self._push_to_frontend(
            "agent_error",
            {
                "trace_id": trace_id,
                "agent_id": agent_id,
                "status": "failed",
                "error": str(error),
                "timestamp": datetime.now().isoformat(),
            },
        )

        logger.error(f"Agent failed: {agent_id} - {error}")
        del self.active_traces[trace_id]

    async def on_llm_start(self, agent_id: str, prompt: str, **kwargs):
        event = {
            "agent_id": agent_id,
            "event_type": "llm_start",
            "prompt": prompt[:500],
            "timestamp": datetime.now().isoformat(),
        }
        await self._push_to_frontend("llm_call", event)
        logger.debug(f"LLM call started for agent: {agent_id}")

    async def on_llm_end(
        self, agent_id: str, response: str, token_usage: Dict[str, int], **kwargs
    ):
        trace_id = kwargs.get("trace_id")
        if trace_id and trace_id in self.active_traces:
            trace = self.active_traces[trace_id]
            trace.token_usage = token_usage

        event = {
            "agent_id": agent_id,
            "event_type": "llm_end",
            "response": response[:500],
            "token_usage": token_usage,
            "timestamp": datetime.now().isoformat(),
        }
        await self._push_to_frontend("llm_call", event)
        logger.debug(f"LLM call completed for agent: {agent_id}, tokens: {token_usage}")

    async def on_tool_start(
        self, agent_id: str, tool_name: str, params: Dict[str, Any], **kwargs
    ):
        event = {
            "agent_id": agent_id,
            "event_type": "tool_start",
            "tool_name": tool_name,
            "params": params,
            "timestamp": datetime.now().isoformat(),
        }
        await self._push_to_frontend("tool_call", event)
        logger.debug(f"Tool call started: {tool_name} for agent: {agent_id}")

    async def on_tool_end(self, agent_id: str, tool_name: str, result: Any, **kwargs):
        event = {
            "agent_id": agent_id,
            "event_type": "tool_end",
            "tool_name": tool_name,
            "result": str(result)[:1000],
            "timestamp": datetime.now().isoformat(),
        }
        await self._push_to_frontend("tool_call", event)
        logger.debug(f"Tool call completed: {tool_name} for agent: {agent_id}")

    async def on_state_change(
        self, agent_id: str, old_state: str, new_state: str, **kwargs
    ):
        event = {
            "agent_id": agent_id,
            "event_type": "state_change",
            "old_state": old_state,
            "new_state": new_state,
            "timestamp": datetime.now().isoformat(),
        }
        await self._push_to_frontend("state_change", event)
        logger.info(f"Agent state changed: {agent_id} {old_state} -> {new_state}")

    async def on_message_send(
        self, source_agent: str, target_agent: str, message: Any, **kwargs
    ):
        msg = AgentMessage(
            message_id=f"msg_{uuid.uuid4().hex[:8]}",
            trace_id=kwargs.get("trace_id", ""),
            source_agent_id=source_agent,
            target_agent_id=target_agent,
            message_type=kwargs.get("message_type", "request"),
            content=message,
        )

        await self.trace_store.save_message(msg)

        await self._push_to_frontend(
            "agent_message",
            {
                "source_agent": source_agent,
                "target_agent": target_agent,
                "message_type": msg.message_type,
                "timestamp": datetime.now().isoformat(),
            },
        )

        logger.debug(f"Message sent: {source_agent} -> {target_agent}")

    async def _push_to_frontend(self, event_type: str, data: Dict[str, Any]):
        if self.websocket_manager:
            await self.websocket_manager.broadcast(
                {
                    "event_type": event_type,
                    "data": data,
                    "timestamp": datetime.now().isoformat(),
                }
            )
