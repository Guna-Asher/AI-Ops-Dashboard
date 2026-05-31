from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dashboard import DashboardWidget
from app.repositories.dashboard import DashboardRepository
from app.schemas.dashboard import WidgetCreate

class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DashboardRepository(db)

    async def list_widgets(self, user_id: int) -> List[DashboardWidget]:
        return await self.repo.get_by_user(user_id)

    async def create_widget(self, widget_in: WidgetCreate, user_id: int) -> DashboardWidget:
        data = widget_in.dict()
        data["user_id"] = user_id
        return await self.repo.create(data)