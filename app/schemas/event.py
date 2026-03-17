from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventCreate(BaseModel):
    source: str
    service: str | None = None
    severity: str | None = None
    message: str
    event_time: datetime
    metadata_json: dict | None = None


class EventRead(BaseModel):
    id: UUID
    source: str
    service: str | None
    severity: str | None
    message: str
    event_time: datetime
    metadata_json: dict | None

    model_config = {"from_attributes": True}