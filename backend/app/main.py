from fastapi import FastAPI
from app.api.v1.endpoints import incidents

app = FastAPI(title="AI Ops Dashboard API", version="0.1.0")

app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["incidents"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}