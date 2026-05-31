from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.dashboard import WidgetCreate, WidgetOut
from app.services.dashboard import DashboardService

router = APIRouter()

@router.get("/widgets", response_model=List[WidgetOut])
async def list_widgets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    service = DashboardService(db)
    return await service.list_widgets(current_user.id)

@router.post("/widgets", response_model=WidgetOut, status_code=201)
async def create_widget(
    *,
    db: AsyncSession = Depends(get_db),
    widget_in: WidgetCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    service = DashboardService(db)
    return await service.create_widget(widget_in, current_user.id)