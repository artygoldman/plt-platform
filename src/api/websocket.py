"""WebSocket hub for real-time updates: agent progress, score changes, alerts."""

import json
import logging
from typing import Dict, Set

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections per user for real-time updates.

    Maintains a registry of active WebSocket connections grouped by user_id,
    enabling broadcasting of messages to specific users or all connected clients.
    """

    def __init__(self):
        """Initialize connection manager with empty connection registry."""
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        """Accept a WebSocket connection and register it for a user.

        Args:
            websocket: FastAPI WebSocket connection object
            user_id: User ID to associate with this connection

        Raises:
            Exception: If accept() fails on the websocket

        TODO: Implement connection acceptance and registry
        """
        if not user_id:
            raise ValueError("user_id cannot be empty")
        if not websocket:
            raise ValueError("websocket cannot be None")

        try:
            await websocket.accept()

            # Initialize user's connection set if needed
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()

            self.active_connections[user_id].add(websocket)
            logger.info(f"WebSocket connected for user {user_id}")

        except Exception as e:
            logger.error(f"Error accepting WebSocket connection: {e}")
            raise

    def disconnect(self, websocket: WebSocket, user_id: str) -> None:
        """Remove a WebSocket connection from the registry.

        Args:
            websocket: WebSocket connection to remove
            user_id: User ID associated with the connection

        Raises:
            ValueError: If user_id is empty or connection not found
        """
        if not user_id:
            raise ValueError("user_id cannot be empty")
        if not websocket:
            raise ValueError("websocket cannot be None")

        try:
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)

                # Clean up empty user sets
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]

                logger.info(f"WebSocket disconnected for user {user_id}")
            else:
                logger.warning(f"Attempted to disconnect unknown user: {user_id}")

        except Exception as e:
            logger.error(f"Error disconnecting WebSocket: {e}")
            raise

    async def send_to_user(self, user_id: str, message: dict) -> None:
        """Send a message to all WebSocket connections for a specific user.

        Args:
            user_id: User ID whose connections to send to
            message: Dictionary message to send (will be JSON encoded)

        Raises:
            ValueError: If user_id is empty or message is None
            Exception: If send fails on any connection

        TODO: Implement send logic with error handling for stale connections
        """
        if not user_id:
            raise ValueError("user_id cannot be empty")
        if not message:
            raise ValueError("message cannot be empty")

        try:
            if user_id not in self.active_connections:
                logger.debug(f"No active connections for user {user_id}")
                return

            disconnected = []
            for websocket in self.active_connections[user_id]:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.warning(f"Error sending to user {user_id}: {e}")
                    disconnected.append(websocket)

            # Remove disconnected connections
            for ws in disconnected:
                self.disconnect(ws, user_id)

            logger.debug(f"Message sent to {len(self.active_connections.get(user_id, set()))} connections for user {user_id}")

        except Exception as e:
            logger.error(f"Error sending message to user {user_id}: {e}")
            raise

    async def broadcast(self, message: dict) -> None:
        """Broadcast a message to all connected WebSocket clients.

        Sends a message to every active connection across all users.

        Args:
            message: Dictionary message to broadcast (will be JSON encoded)

        Raises:
            ValueError: If message is None
            Exception: If broadcast fails

        TODO: Implement broadcast logic with connection cleanup
        """
        if not message:
            raise ValueError("message cannot be empty")

        try:
            total_sent = 0
            disconnected = []

            for user_id, connections in self.active_connections.items():
                for websocket in connections:
                    try:
                        await websocket.send_json(message)
                        total_sent += 1
                    except Exception as e:
                        logger.warning(f"Error broadcasting to user {user_id}: {e}")
                        disconnected.append((websocket, user_id))

            # Remove disconnected connections
            for ws, uid in disconnected:
                self.disconnect(ws, uid)

            logger.debug(f"Broadcast sent to {total_sent} total connections")

        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
            raise


# Global connection manager instance
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, user_id: str) -> None:
    """WebSocket endpoint for real-time updates.

    Path: /ws/v1/live/{user_id}

    Establishes and maintains WebSocket connection for a user, listening for
    incoming messages and broadcasting updates from the agent system.

    Args:
        websocket: FastAPI WebSocket connection
        user_id: User ID for this connection

    Message format (incoming from client):
        {
            "type": "ping" | "subscribe" | "action",
            "data": {...}
        }

    Message format (outgoing to client):
        {
            "type": "pong" | "update" | "alert" | "agent_progress",
            "data": {...},
            "timestamp": "ISO-8601"
        }

    Raises:
        WebSocketDisconnect: When client disconnects (normal flow)
        Exception: If connection or message handling fails

    TODO: Implement message routing and update handling
    """
    if not user_id:
        await websocket.close(code=1008, reason="user_id required")
        return

    try:
        await manager.connect(websocket, user_id)

        # Listen for incoming messages from client
        while True:
            try:
                data = await websocket.receive_json()
                msg_type = data.get("type", "unknown")

                logger.debug(f"WebSocket message from {user_id}: {msg_type}")

                # TODO: Implement message routing
                # Handle different message types:
                # - "ping": respond with "pong"
                # - "subscribe": subscribe to specific event types
                # - "action": handle client-initiated actions
                # - other: log warning for unknown types

                # For now, echo pong for ping
                if msg_type == "ping":
                    await websocket.send_json(
                        {
                            "type": "pong",
                            "timestamp": "2026-03-27T00:00:00Z",
                        }
                    )

            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from {user_id}")
                await websocket.send_json(
                    {
                        "type": "error",
                        "detail": "Invalid JSON",
                        "timestamp": "2026-03-27T00:00:00Z",
                    }
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        logger.info(f"WebSocket disconnected for user {user_id}")

    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(websocket, user_id)
        await websocket.close(code=1011, reason="Internal server error")
