from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes_events import router as events_router
from app.core.db import Base, engine
from app.models import event, incident  # noqa: F401 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Incident Triage API",
    description="API for managing and triaging incidents",
    lifespan=lifespan,
)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(events_router)
