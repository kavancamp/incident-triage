# Incident Triage API

A backend service that ingests events and automatically groups related signals into incidents, reducing alert noise and improving observability.

## Problem

Monitoring systems often generate large volumes of alerts. Without grouping, teams are forced to manually correlate related events, leading to alert fatigue and slower response times.

## Solution

This service ingests raw events and groups them into incidents based on shared attributes (e.g., service and severity), creating a structured view of system issues.

## Features

- Event ingestion via REST API
- Automatic incident grouping (service + severity)
- Relational data model (events → incidents)
- Incident tracking with status and timestamps
- PostgreSQL + SQLAlchemy backend
- FastAPI-based API with validation via Pydantic

### Tech stack:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Pydantic

### Architecture

Event → Evaluation → Incident Assignment → Persistence

- Events are ingested via `/events`
- The system checks for an existing open incident
- If found, the event is attached
- Otherwise, a new incident is created

## 🔁 Example

POST /events

Event 1:

- service: auth-api
- severity: critical
  → creates Incident A

Event 2:

- service: auth-api
- severity: critical
  → attaches to Incident A

Event 3:

- service: payments-api
- severity: warning
  → creates Incident B

## API

### Events

- POST /events → ingest event
- GET /events → list events

### Incidents

- GET /incidents → list incidents with related events
- GET /incidents/{id} → get a single incident

## Run locally

### 1. Start the database:

```bash
docker compose up -d
```

### 2. Run the API:

```bash
uvicorn app.main:app --reload
```

### 3. Open docs

http://127.0.0.1:8000/docs

## Example Event

{
"source": "alertmanager",
"service": "auth-api",
"severity": "critical",
"message": "Spike in 500 responses",
"event_time": "2026-03-20T15:30:00Z"
}

## Future Work

- Smarter incident grouping (message similarity, time windows)
- Incident status updates (open → resolved)
- Filtering and search (by service, severity, status)
- AI-assisted clustering of events
- Alert deduplication

Inspired by real-world monitoring systems (e.g., Datadog, PagerDuty) and my experience working with operational alert systems.
