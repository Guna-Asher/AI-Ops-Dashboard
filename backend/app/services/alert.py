from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert
from app.repositories.alert import AlertRepository
from app.schemas.alert import AlertCreate, AlertUpdate

class AlertService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AlertRepository(db)

    async def list_alerts(self) -> List[Alert]:
        return await self.repo.get_multi()

    async def create_alert(self, alert_in: AlertCreate, user_id: int) -> Alert:
        data = alert_in.dict()
        data["created_by"] = user_id
        return await self.repo.create(data)

    async def update_alert(self, alert_id: int, update_in: AlertUpdate) -> Optional[Alert]:
        return await self.repo.update(alert_id, update_in.dict(exclude_unset=True))

    async def delete_alert(self, alert_id: int) -> bool:
        return await self.repo.delete(alert_id)