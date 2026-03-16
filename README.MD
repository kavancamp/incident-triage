# Incident Triage API

A backend service for ingesting operational events and grouping them into incidents.

Tech stack:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker

## Run locally

Start the database:

docker compose up -d

Run the API:

uvicorn app.main:app --reload
