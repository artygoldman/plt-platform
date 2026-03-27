from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProtocolResponse(BaseModel):
    """Schema for a longevity protocol."""

    id: UUID
    version: int
    status: str
    nutrition_plan: dict | None = None
    supplement_plan: dict | None = None
    fitness_plan: dict | None = None
    sleep_protocol: dict | None = None
    environment: dict | None = None
    medical_actions: dict | None = None
    valid_from: date | None = None
    valid_until: date | None = None
    approved_by: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContractItem(BaseModel):
    """A single contract item (actionable commitment)."""

    id: str
    text: str
    category: str
    source_agent: str
    completed: bool = False
    impact_score: float = 0


class ContractResponse(BaseModel):
    """Schema for daily contracts."""

    id: UUID
    date: date
    contracts: list[ContractItem]
    completion_rate: float
    longevity_delta: float | None = None

    model_config = ConfigDict(from_attributes=True)
