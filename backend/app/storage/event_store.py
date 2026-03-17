import logging
import asyncio
import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any

from app.models.events import OpenCodeEvent, EventCategory, EventType
from app.models.agent_status import AgentOnlineStatus, AgentStatus

logger = logging.getLogger(__name__)


class EventStore:
    def __init__(self, database_url: str, redis_url: str = ""):
        self.database_url = database_url
        self.db_path = database_url.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opencode_events (
                event_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                session_id TEXT,
                
                event_category TEXT NOT NULL,
                event_type TEXT NOT NULL,
                
                input_data TEXT,
                output_data TEXT,
                
                timestamp TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_agent ON opencode_events(agent_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_type ON opencode_events(event_type)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_timestamp ON opencode_events(timestamp)
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opencode_agent_status (
                agent_id TEXT PRIMARY KEY,
                agent_name TEXT,
                status TEXT NOT NULL,
                last_seen TEXT,
                current_session TEXT,
                total_events INTEGER DEFAULT 0,
                event_counts TEXT DEFAULT '{}',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Event database initialized successfully")

    async def init_db(self):
        pass

    async def close(self):
        pass

    async def save_event(self, event: OpenCodeEvent) -> str:
        def _save():
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO opencode_events 
                    (event_id, agent_id, session_id, event_category, event_type,
                     input_data, output_data, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        event.event_id,
                        event.agent_id,
                        event.session_id,
                        event.event_category.value,
                        event.event_type.value,
                        json.dumps(event.input_data),
                        json.dumps(event.output_data),
                        event.timestamp.isoformat(),
                    ),
                )

                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to save event: {e}")
                raise

        await asyncio.get_event_loop().run_in_executor(None, _save)
        await self._update_agent_status(event.agent_id, event.event_type.value)
        logger.debug(f"Event saved: {event.event_id} from {event.agent_id}")

    async def get_event(self, event_id: str) -> Optional[OpenCodeEvent]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM opencode_events WHERE event_id = ?",
                (event_id,),
            )

            row = cursor.fetchone()
            conn.close()

            if row:
                return self._row_to_event(row)
            return None

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def get_events(
        self,
        agent_id: Optional[str] = None,
        event_type: Optional[str] = None,
        event_category: Optional[str] = None,
        session_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[OpenCodeEvent]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = "SELECT * FROM opencode_events WHERE 1=1"
            params = []

            if agent_id:
                query += " AND agent_id = ?"
                params.append(agent_id)
            if event_type:
                query += " AND event_type = ?"
                params.append(event_type)
            if event_category:
                query += " AND event_category = ?"
                params.append(event_category)
            if session_id:
                query += " AND session_id = ?"
                params.append(session_id)
            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time.isoformat())
            if end_time:
                query += " AND timestamp <= ?"
                params.append(end_time.isoformat())

            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            return [self._row_to_event(row) for row in rows]

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM opencode_agent_status WHERE agent_id = ?",
                (agent_id,),
            )

            row = cursor.fetchone()
            conn.close()

            if row:
                return self._row_to_agent_status(row)
            return None

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def get_all_agents(self) -> List[AgentStatus]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM opencode_agent_status ORDER BY last_seen DESC"
            )

            rows = cursor.fetchall()
            conn.close()

            return [self._row_to_agent_status(row) for row in rows]

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def _update_agent_status(self, agent_id: str, event_type: str):
        def _update():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            now = datetime.now().isoformat()

            cursor.execute(
                """
                INSERT INTO opencode_agent_status (agent_id, agent_name, status, last_seen, total_events, event_counts)
                VALUES (?, ?, 'online', ?, 1, ?)
                ON CONFLICT(agent_id) DO UPDATE SET
                    agent_name = excluded.agent_name,
                    status = 'online',
                    last_seen = excluded.last_seen,
                    total_events = total_events + 1,
                    event_counts = json_set(
                        json_extract(event_counts, '$') || '{}'
                    ) || excluded.event_counts
                )
            """,
                (agent_id, agent_id, now, json.dumps({event_type: 1}), agent_id, now),
            )

            cursor.execute(
                """
                UPDATE opencode_agent_status 
                SET last_seen = ?, 
                    total_events = total_events + 1,
                    event_counts = json_set(json_patch(event_counts, '$.' || '{}', ?))
                WHERE agent_id = ?
                """,
                (now, f"$.{event_type}", 1, agent_id),
            )

            conn.commit()
            conn.close()

        await asyncio.get_event_loop().run_in_executor(None, _update)

    async def update_agent_heartbeat(self, agent_id: str, agent_name: str = "online"):
        def _update():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            now = datetime.now().isoformat()

            cursor.execute(
                """
                INSERT INTO opencode_agent_status (agent_id, agent_name, status, last_seen, total_events, event_counts)
                VALUES (?, ?, 'online', ?, 0, '{}')
                ON CONFLICT(agent_id) DO UPDATE SET
                    agent_name = excluded.agent_name,
                    status = 'online',
                    last_seen = excluded.last_seen,
                    total_events = excluded.total_events,
                    event_counts = excluded.event_counts,
                )
            """,
                (agent_id, agent_name, now, agent_id, agent_name, now),
            )

            cursor.execute(
                """
                UPDATE opencode_agent_status 
                SET status = 'online', last_seen = ?, agent_name = ?
                WHERE agent_id = ?
                """,
                (now, agent_name, agent_id),
            )

            conn.commit()
            conn.close()

        await asyncio.get_event_loop().run_in_executor(None, _update)

    async def set_agent_offline(self, agent_id: str, reason: str = "timeout"):
        def _update():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE opencode_agent_status 
                SET status = 'offline', agent_name = ?
                WHERE agent_id = ?
                """,
                (reason, agent_id),
            )

            conn.commit()
            conn.close()

        await asyncio.get_event_loop().run_in_executor(None, _update)

    async def cleanup_old_events(self, days: int = 30):
        def _cleanup():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM opencode_events WHERE timestamp < datetime('now', ?)",
                (f"-{days} days",),
            )

            deleted = cursor.rowcount
            conn.commit()
            conn.close()

            logger.info(f"Cleaned up {deleted} events older than {days} days")
            return {"events_deleted": deleted}

        return await asyncio.get_event_loop().run_in_executor(None, _cleanup)

    async def get_event_statistics(self) -> Dict[str, Any]:
        def _get():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT 
                    event_category,
                    event_type,
                    COUNT(*) as count
                FROM opencode_events
                GROUP BY event_category, event_type
                ORDER BY count DESC
                """
            )

            rows = cursor.fetchall()
            conn.close()

            stats = {
                "by_category": {},
                "by_type": {},
                "total": 0,
            }

            for row in rows:
                category = row[0]
                event_type = row[1]
                count = row[2]

                stats["by_category"][category] = (
                    stats["by_category"].get(category, 0) + count
                )
                stats["by_type"][event_type] = (
                    stats["by_type"].get(event_type, 0) + count
                )
                stats["total"] += count

            return stats

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    def _row_to_event(self, row) -> OpenCodeEvent:
        return OpenCodeEvent(
            event_id=row[0],
            agent_id=row[1],
            session_id=row[2],
            event_category=EventCategory(row[3]),
            event_type=EventType(row[4]),
            input_data=json.loads(row[5]) if row[5] else {},
            output_data=json.loads(row[6]) if row[6] else {},
            timestamp=datetime.fromisoformat(row[7]),
        )

    def _row_to_agent_status(self, row) -> AgentStatus:
        return AgentStatus(
            agent_id=row[0],
            agent_name=row[1],
            status=AgentOnlineStatus(row[2]),
            last_seen=datetime.fromisoformat(row[3]) if row[3] else None,
            current_session=row[4],
            total_events=row[5] or 0,
            event_counts=json.loads(row[6]) if row[6] else {},
        )
