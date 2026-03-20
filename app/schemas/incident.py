from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class IncidentCreate(BaseModel):
    service: str
    severity: str


class IncidentRead(BaseModel):
    id: UUID
    service: str
    severity: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}