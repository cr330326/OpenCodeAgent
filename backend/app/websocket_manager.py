from typing import List, Dict, Any
from fastapi import WebSocket
import logging
import json

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(
            f"WebSocket connected. Total connections: {len(self.active_connections)}"
        )

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(
            f"WebSocket disconnected. Total connections: {len(self.active_connections)}"
        )

    async def broadcast(self, message: Dict[str, Any]):
        if not self.active_connections:
            return

        message_json = json.dumps(message)
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Failed to send message to WebSocket: {e}")
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

    async def send_to_session(self, session_id: str, message: Dict[str, Any]):
        message["session_id"] = session_id
        await self.broadcast(message)


ws_manager = WebSocketManager()
