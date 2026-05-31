from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.log import LogCreate, LogOut
from app.services.log import LogService

router = APIRouter()

@router.get("/", response_model=List[LogOut])
async def list_logs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    incident_id: int = Query(None, description="Filter by incident ID"),
) -> Any:
    service = LogService(db)
    return await service.list_logs(skip=skip, limit=limit, incident_id=incident_id)

@router.post("/", response_model=LogOut, status_code=201)
async def create_log(
    *,
    db: AsyncSession = Depends(get_db),
    log_in: LogCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    service = LogService(db)
    log = await service.create_log(log_in)
    return log

@router.get("/{log_id}", response_model=LogOut)
async def get_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    service = LogService(db)
    log = await service.get_log(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log