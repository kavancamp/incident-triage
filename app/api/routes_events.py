from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.db import get_db
from app.models.event import Event
from app.models.incident import Incident
from app.schemas.event import EventCreate, EventRead
from app.services.incident_service import find_or_create_incident
from app.services.triage_service import update_incident_priority

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventRead)
def create_event(payload: EventCreate, db: Session = Depends(get_db)) -> Event:
    event = Event(**payload.model_dump())
    
    incident = find_or_create_incident(
        db, 
        event
    )
    event.incident_id = incident.id
    
    db.add(event)
    db.flush()
    
    stmt = (
        select(Incident)
        .options(selectinload(Incident.events))
        .where(Incident.id == incident.id)
    )
    
    incident_with_events = db.scalar(stmt)
    
    update_incident_priority(incident_with_events)
    
    db.commit()
    db.refresh(event)
    return event

@router.get("", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)) -> list[Event]:
    stmt = select(Event).order_by(Event.event_time.desc())
    return list(db.scalars(stmt).all())

