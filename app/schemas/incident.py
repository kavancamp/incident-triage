from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.event import EventRead


class IncidentCreate(BaseModel):
    service: str
    severity: str


class IncidentRead(BaseModel):
    id: UUID
    service: str
    severity: str
    status: str
    priority_score: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
    
class IncidentDetailRead(BaseModel):
    id: UUID
    service: str
    severity:str
    status: str
    priority_score: int
    created_at: datetime
    updated_at: datetime
    events: list[EventRead]
    model_config = {"from_attributes": True}
    
class IncidentStatusUpdate(BaseModel):
    status: str