from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.log import LogEntry
from app.repositories.base import BaseRepository

class LogRepository(BaseRepository[LogEntry]):
    def __init__(self, db: AsyncSession):
        super().__init__(LogEntry, db)

    async def get_by_incident(self, incident_id: int, skip: int = 0, limit: int = 100) -> List[LogEntry]:
        result = await self.db.execute(
            select(LogEntry)
            .where(LogEntry.incident_id == incident_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()