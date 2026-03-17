from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventRead

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventRead)
def create_event(payload: EventCreate, db: Session = Depends(get_db)) -> Event:
    event = Event(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)) -> list[Event]:
    stmt = select(Event).order_by(Event.event_time.desc())
    return list(db.scalars(stmt).all())