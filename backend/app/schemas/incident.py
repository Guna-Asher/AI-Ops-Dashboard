from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.db.models.incident import Severity, Status

class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: Severity = Severity.LOW
    status: Status = Status.OPEN

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[Severity] = None
    status: Optional[Status] = None

class IncidentInDB(IncidentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # this allows conversion from ORM objects