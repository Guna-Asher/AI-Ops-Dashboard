from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.incident import IncidentCreate, IncidentUpdate, IncidentOut
from app.services.incident import IncidentService
from app.services.event_bus import EventBus

router = APIRouter()

@router.get("/", response_model=List[IncidentOut])
async def list_incidents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    service = IncidentService(db)
    return await service.list_incidents(skip=skip, limit=limit)

@router.post("/", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
async def create_incident(
    *,
    db: AsyncSession = Depends(get_db),
    incident_in: IncidentCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    service = IncidentService(db)
    incident = await service.create_incident(incident_in, user_id=current_user.id)
    # Publish event for AI analysis
    event_bus = EventBus(db)
    await event_bus.publish_incident_created(incident.id)
    return incident

@router.get("/{incident_id}", response_model=IncidentOut)
async def get_incident(
    incident_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    service = IncidentService(db)
    incident = await service.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.put("/{incident_id}", response_model=IncidentOut)
async def update_incident(
    incident_id: int,
    incident_in: IncidentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    service = IncidentService(db)
    incident = await service.update_incident(incident_id, incident_in)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incident(
    incident_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    service = IncidentService(db)
    # Superusers can delete anything; normal users can only delete their assigned incidents
    if not current_user.is_superuser:
        incident = await service.get_incident(incident_id)
