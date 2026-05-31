from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.incident import Incident
from app.repositories.incident import IncidentRepository
from app.schemas.incident import IncidentCreate, IncidentUpdate

class IncidentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = IncidentRepository(db)

    async def list_incidents(self, skip: int = 0, limit: int = 100) -> List[Incident]:
        return await self.repo.get_multi(skip=skip, limit=limit)

    async def create_incident(self, incident_in: IncidentCreate, user_id: int) -> Incident:
        data = incident_in.dict(exclude_unset=True)
        data["assigned_to"] = user_id  # auto-assign creator
        return await self.repo.create(data)

    async def get_incident(self, incident_id: int) -> Optional[Incident]:
        return await self.repo.get(incident_id)

    async def update_incident(self, incident_id: int, update_in: IncidentUpdate) -> Optional[Incident]:
        update_data = update_in.dict(exclude_unset=True)
        return await self.repo.update(incident_id, update_data)

    async def delete_incident(self, incident_id: int) -> bool:
        return await self.repo.delete(incident_id)