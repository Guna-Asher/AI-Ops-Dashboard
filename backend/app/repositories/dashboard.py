from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.dashboard import DashboardWidget
from app.repositories.base import BaseRepository

class DashboardRepository(BaseRepository[DashboardWidget]):
    def __init__(self, db: AsyncSession):
        super().__init__(DashboardWidget, db)

    async def get_by_user(self, user_id: int) -> List[DashboardWidget]:
        result = await self.db.execute(
            select(DashboardWidget).where(DashboardWidget.user_id == user_id)
        )
        return result.scalars().all()