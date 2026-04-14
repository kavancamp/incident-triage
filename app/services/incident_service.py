from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.incident import Incident

def find_or_create_incident(db: Session, event: Event) -> Incident:
    stmt = select(Incident).where(
        Incident.service == event.service,
        Incident.severity == event.severity,
        Incident.status == "open",   
    )
    
    existing_incident = db.scalars(stmt).first()
    
    if existing_incident:
        return existing_incident
    
    new_incident = Incident(
        service=event.service or "unknown",
        severity=event.severity or "unknown",
        status="open"
    )
    
    db.add(new_incident)
    db.flush()
    
    return new_incident
