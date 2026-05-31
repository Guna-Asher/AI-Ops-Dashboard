from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.log import LogEntry
from app.repositories.log import LogRepository
from app.schemas.log import LogCreate

class LogService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = LogRepository(db)

    async def list_logs(self, skip: int = 0, limit: int = 100, incident_id: Optional[int] = None) -> List[LogEntry]:
        if incident_id is not None:
            return await self.repo.get_by_incident(incident_id, skip=skip, limit=limit)
        return await self.repo.get_multi(skip=skip, limit=limit)

    async def create_log(self, log_in: LogCreate) -> LogEntry:
        return await self.repo.create(log_in.dict())

    async def get_log(self, log_id: int) -> Optional[LogEntry]:
        return await self.repo.get(log_id)