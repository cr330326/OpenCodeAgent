from typing import List, Optional, Dict, Any
from datetime import datetime
import sqlite3
import json
import logging
import asyncio

from app.models import AgentTrace, AgentMessage, AgentMetrics

logger = logging.getLogger(__name__)


class TraceStore:
    def __init__(self, database_url: str, redis_url: str = ""):
        self.database_url = database_url
        self.db_path = database_url.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_traces (
                trace_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                parent_trace_id TEXT,
                agent_id TEXT NOT NULL,
                agent_name TEXT,
                agent_type TEXT,
                status TEXT NOT NULL,
                input_data TEXT,
                output_data TEXT,
                error_info TEXT,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                duration_ms INTEGER,
                token_usage TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_traces_session ON agent_traces(session_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_traces_agent ON agent_traces(agent_id)
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_messages (
                message_id TEXT PRIMARY KEY,
                trace_id TEXT,
                source_agent_id TEXT NOT NULL,
                target_agent_id TEXT NOT NULL,
                message_type TEXT,
                content TEXT,
                timestamp TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")

    async def init_db(self):
        pass

    async def close(self):
        pass

    async def save_trace(self, trace: AgentTrace):
        def _save():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO agent_traces 
                (trace_id, session_id, parent_trace_id, agent_id, agent_name, agent_type,
                 status, input_data, output_data, error_info, started_at, ended_at,
                 duration_ms, token_usage, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    trace.trace_id,
                    trace.session_id,
                    trace.parent_trace_id,
                    trace.agent_id,
                    trace.agent_name,
                    trace.agent_type,
                    trace.status,
                    json.dumps(trace.input_data),
                    json.dumps(trace.output_data) if trace.output_data else None,
                    json.dumps(trace.error_info) if trace.error_info else None,
                    trace.started_at.isoformat(),
                    trace.ended_at.isoformat() if trace.ended_at else None,
                    trace.duration_ms,
                    json.dumps(trace.token_usage),
                    json.dumps(trace.metadata),
                ),
            )

            conn.commit()
            conn.close()

        await asyncio.get_event_loop().run_in_executor(None, _save)

    async def get_session_traces(self, session_id: str) -> List[AgentTrace]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM agent_traces 
                WHERE session_id = ? 
                ORDER BY started_at ASC
            """,
                (session_id,),
            )

            rows = cursor.fetchall()
            conn.close()

            return [self._row_to_trace(row) for row in rows]

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def get_trace(self, trace_id: str) -> Optional[AgentTrace]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM agent_traces WHERE trace_id = ?
            """,
                (trace_id,),
            )

            row = cursor.fetchone()
            conn.close()

            return self._row_to_trace(row) if row else None

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def save_message(self, message: AgentMessage):
        def _save():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO agent_messages 
                (message_id, trace_id, source_agent_id, target_agent_id, 
                 message_type, content, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    message.message_id,
                    message.trace_id,
                    message.source_agent_id,
                    message.target_agent_id,
                    message.message_type,
                    json.dumps(message.content),
                    message.timestamp.isoformat(),
                ),
            )

            conn.commit()
            conn.close()

        await asyncio.get_event_loop().run_in_executor(None, _save)

    async def get_agent_metrics(
        self, agent_id: str, time_window: str = "24h"
    ) -> AgentMetrics:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            time_filter = {
                "1h": "-1 hour",
                "24h": "-1 day",
                "7d": "-7 days",
                "30d": "-30 days",
            }.get(time_window, "-1 day")

            cursor.execute(
                """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    AVG(duration_ms) as avg_duration,
                    total_tokens
                FROM agent_traces 
                WHERE agent_id = ? 
                AND started_at >= datetime('now', ?)
            """,
                (agent_id, time_filter),
            )

            row = cursor.fetchone()
            conn.close()

            if row and row[0] > 0:
                total = row[0] or 0
                success = row[1] or 0
                failed = row[2] or 0
                return AgentMetrics(
                    agent_id=agent_id,
                    time_window=time_window,
                    total_executions=total,
                    success_count=success,
                    failed_count=failed,
                    avg_duration_ms=float(row[3] or 0),
                    success_rate=success / total if total > 0 else 0,
                    error_rate=failed / total if total > 0 else 0,
                )
            return AgentMetrics(agent_id=agent_id, time_window=time_window)

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def get_all_traces(
        self,
        limit: int = 50,
        offset: int = 0,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[AgentTrace]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = "SELECT * FROM agent_traces WHERE 1=1"
            params = []

            if agent_id:
                query += " AND agent_id = ?"
                params.append(agent_id)
            if status:
                query += " AND status = ?"
                params.append(status)

            query += " ORDER BY started_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            return [self._row_to_trace(row) for row in rows]

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def get_statistics(self) -> Dict[str, Any]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT 
                    COUNT(*) as total_traces,
                    COUNT(DISTINCT agent_id) as total_agents,
                    COUNT(DISTINCT session_id) as total_sessions,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_count,
                    AVG(duration_ms) as avg_duration
                FROM agent_traces
            """
            )
            row = cursor.fetchone()
            conn.close()

            return {
                "total_traces": row[0] or 0,
                "total_agents": row[1] or 0,
                "total_sessions": row[2] or 0,
                "success_count": row[3] or 0,
                "failed_count": row[4] or 0,
                "avg_duration_ms": float(row[5] or 0),
            }

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def cleanup_old_data(self, days: int = 30):
        def _cleanup():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM agent_messages 
                WHERE timestamp < datetime('now', ?)
            """,
                (f"-{days} days",),
            )
            messages_deleted = cursor.rowcount

            cursor.execute(
                """
                DELETE FROM agent_traces 
                WHERE started_at < datetime('now', ?)
            """,
                (f"-{days} days",),
            )
            traces_deleted = cursor.rowcount

            conn.commit()
            conn.close()

            logger.info(
                f"Cleanup completed: {traces_deleted} traces, {messages_deleted} messages deleted"
            )
            return {
                "traces_deleted": traces_deleted,
                "messages_deleted": messages_deleted,
            }

        return await asyncio.get_event_loop().run_in_executor(None, _cleanup)

    def _row_to_trace(self, row) -> AgentTrace:
        return AgentTrace(
            trace_id=row[0],
            session_id=row[1],
            parent_trace_id=row[2],
            agent_id=row[3],
            agent_name=row[4],
            agent_type=row[5],
            status=row[6],
            input_data=json.loads(row[7]) if row[7] else {},
            output_data=json.loads(row[8]) if row[8] else None,
            error_info=json.loads(row[9]) if row[9] else None,
            started_at=datetime.fromisoformat(row[10]),
            ended_at=datetime.fromisoformat(row[11]) if row[11] else None,
            duration_ms=row[12],
            token_usage=json.loads(row[13]) if row[13] else {},
            metadata=json.loads(row[14]) if row[14] else {},
        )
