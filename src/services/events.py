"""Redis event bus for inter-service communication."""

import json
import logging
from typing import Any, Callable, Dict, Optional

import redis.asyncio as redis

from src.core.config import get_settings

logger = logging.getLogger(__name__)

# Event types used throughout the platform
VALID_EVENTS = {
    "new_bloodwork",  # New blood test results uploaded
    "oura_sync",  # Oura Ring data synced
    "apple_health_sync",  # Apple Health data synced
    "daily_morning",  # Daily morning trigger
    "anomaly_detected",  # Health anomaly detected
    "contract_completed",  # Daily contract completed
    "veto_triggered",  # Veto event triggered
    "score_updated",  # Longevity score recalculated
    "protocol_changed",  # User protocol updated
    "inventory_low",  # Supplement inventory low
    "supplement_expired",  # Supplement past expiration
    "health_alert",  # General health alert
    "agent_progress",  # Agent task progress update
}


class EventBus:
    """Redis-backed event bus for pub/sub messaging between services."""

    def __init__(self):
        """Initialize event bus (connection created on connect())."""
        self._redis: Optional[redis.Redis] = None
        self._subscriptions: Dict[str, Callable] = {}

    async def connect(self) -> None:
        """Establish connection to Redis.

        Creates async Redis connection using URL from config.

        Raises:
            Exception: If Redis connection fails
        """
        try:
            settings = get_settings()
            self._redis = await redis.from_url(settings.redis_url, decode_responses=True)
            await self._redis.ping()
            logger.info("EventBus connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self) -> None:
        """Close Redis connection.

        Safe to call even if not connected.
        """
        if self._redis:
            try:
                await self._redis.close()
                logger.info("EventBus disconnected from Redis")
            except Exception as e:
                logger.error(f"Error disconnecting from Redis: {e}")

    async def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        """Publish an event to the bus.

        Publishes event as JSON to a Redis channel named after the event type.
        Other services subscribe to these channels.

        Args:
            event_type: Type of event (must be in VALID_EVENTS)
            data: Event payload dictionary

        Raises:
            ValueError: If event_type is invalid or data is None
            Exception: If Redis publish fails

        TODO: Add event validation and error handling
        """
        if not event_type:
            raise ValueError("event_type cannot be empty")
        if event_type not in VALID_EVENTS:
            raise ValueError(f"Invalid event_type: {event_type}")
        if not data:
            raise ValueError("data cannot be None or empty")

        if not self._redis:
            raise RuntimeError("EventBus not connected to Redis")

        try:
            channel = f"event:{event_type}"
            payload = json.dumps(data)
            await self._redis.publish(channel, payload)
            logger.debug(f"Published event: {event_type} to channel: {channel}")
        except Exception as e:
            logger.error(f"Error publishing event {event_type}: {e}")
            raise

    async def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to events of a specific type.

        Registers a callback function to be called when events of a type are published.

        Args:
            event_type: Type of event to subscribe to (must be in VALID_EVENTS)
            callback: Async callable to invoke on event (receives event data dict)

        Raises:
            ValueError: If event_type is invalid or callback is not callable
            Exception: If Redis subscribe fails

        TODO: Implement actual Redis subscription with callback registry
        """
        if not event_type:
            raise ValueError("event_type cannot be empty")
        if event_type not in VALID_EVENTS:
            raise ValueError(f"Invalid event_type: {event_type}")
        if not callable(callback):
            raise ValueError("callback must be callable")

        try:
            self._subscriptions[event_type] = callback
            logger.info(f"Subscribed to event type: {event_type}")

            # TODO: Implement actual Redis Pub/Sub
            # 1. Create Redis pubsub object
            # 2. Subscribe to channel for this event_type
            # 3. Create background task to listen for messages
            # 4. When message received, deserialize and call callback
            # 5. Handle subscription lifecycle

        except Exception as e:
            logger.error(f"Error subscribing to event {event_type}: {e}")
            raise

    async def unsubscribe(self, event_type: str) -> None:
        """Unsubscribe from events of a specific type.

        Args:
            event_type: Type of event to unsubscribe from

        Raises:
            ValueError: If event_type is invalid or not subscribed
        """
        if not event_type:
            raise ValueError("event_type cannot be empty")
        if event_type not in self._subscriptions:
            raise ValueError(f"Not subscribed to event_type: {event_type}")

        try:
            del self._subscriptions[event_type]
            logger.info(f"Unsubscribed from event type: {event_type}")
        except Exception as e:
            logger.error(f"Error unsubscribing from event {event_type}: {e}")
            raise


# Global event bus instance
event_bus = EventBus()
