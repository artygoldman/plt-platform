from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AgentRunRequest(BaseModel):
    """Schema for triggering an agent cycle."""

    user_id: UUID
    trigger_type: Literal["new_data", "daily", "user_query", "alert"]
    trigger_data: dict = {}


class AgentDecisionResponse(BaseModel):
    """Schema for a single agent decision."""

    id: UUID
    agent_id: str
    confidence: int | None = None
    was_vetoed: bool
    output_data: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentSessionResponse(BaseModel):
    """Schema for agent session with all decisions."""

    id: UUID
    status: str
    trigger_type: str
    started_at: datetime
    completed_at: datetime | None = None
    total_tokens: int
    decisions: list[AgentDecisionResponse] = []

    model_config = ConfigDict(from_attributes=True)
