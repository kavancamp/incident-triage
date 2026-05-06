from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.incident import Incident
from app.schemas.incident import IncidentRead, IncidentDetailRead,IncidentStatusUpdate
from sqlalchemy.orm import Session, selectinload

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[IncidentRead])
def list_incidents(
    status: str | None = None,
    service: str | None = None, 
    severity: str | None = None,
    db: Session = Depends(get_db),
    ) -> list[Incident]:
    stmt = select(Incident)
    
    if status:
        stmt = stmt.where(Incident.status == status)
        
    if service:
        stmt = stmt.where(Incident.service == service)
        
    if severity:
        stmt = stmt.where(Incident.severity == severity)
    
    stmt = stmt.order_by(
        Incident.priority_score.desc(),
        Incident.updated_at.desc(),
    )
    
    return list(db.scalars(stmt).all())

@router.get("/next", response_model=IncidentRead)
def get_next_incident(db: Session = Depends(get_db)) -> Incident:
    stmt = (
        select(Incident)
        .where(Incident.status.in_(("open", "investigating")))
        .order_by(
            Incident.priority_score.desc(),
            Incident.updated_at.desc(),
        )
    )

    incident = db.scalar(stmt)

    if incident is None:
        raise HTTPException(status_code=404, detail="No active incidents found")

    return incident

@router.get("/{incident_id}", response_model=IncidentDetailRead)
def get_incident(incident_id: UUID, db: Session = Depends(get_db)) -> Incident:
    stmt = (
        select(Incident)
        .options(selectinload(Incident.events))
        .where(Incident.id == incident_id)
    )

    incident = db.scalar(stmt)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@router.patch("/{incident_id}", response_model=IncidentRead)
def update_incident_status(
    incident_id: UUID,
    payload: IncidentStatusUpdate,
    db: Session = Depends(get_db),
) -> Incident:
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    allowed_statuses = {"open", "investigating", "resolved"}

    if payload.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(sorted(allowed_statuses))}",
        )

    incident.status = payload.status
    db.commit()
    db.refresh(incident)

    return incident