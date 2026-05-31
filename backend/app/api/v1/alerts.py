from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertUpdate, AlertOut
from app.services.alert import AlertService

router = APIRouter()

@router.get("/", response_model=List[AlertOut])
async def list_alerts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    service = AlertService(db)
    return await service.list_alerts()

@router.post("/", response_model=AlertOut, status_code=201)
async def create_alert(
    *,
    db: AsyncSession = Depends(get_db),
    alert_in: AlertCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    service = AlertService(db)
    return await service.create_alert(alert_in, current_user.id)

@router.put("/{alert_id}", response_model=AlertOut)
async def update_alert(
    alert_id: int,
    alert_in: AlertUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    service = AlertService(db)
    alert = await service.update_alert(alert_id, alert_in)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.delete("/{alert_id}", status_code=204)
async def delete_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    service = AlertService(db)
    success = await service.delete_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")