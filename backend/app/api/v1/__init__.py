from fastapi import APIRouter

from app.api.v1 import auth, incidents, logs, dashboards, alerts

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
router.include_router(logs.router, prefix="/logs", tags=["logs"])
router.include_router(dashboards.router, prefix="/dashboards", tags=["dashboards"])
router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])