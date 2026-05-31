from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert import Alert
from app.repositories.base import BaseRepository

class AlertRepository(BaseRepository[Alert]):
    def __init__(self, db: AsyncSession):
        super().__init__(Alert, db)