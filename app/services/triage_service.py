from app.models.incident import Incident


SEVERITY_WEIGHTS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def calculate_priority_score(incident: Incident) -> int:
    severity_weight = SEVERITY_WEIGHTS.get(incident.severity.lower(), 0)
    event_count = len(incident.events)

    return severity_weight + min(event_count, 5)


def update_incident_priority(incident: Incident) -> None:
    incident.priority_score = calculate_priority_score(incident)