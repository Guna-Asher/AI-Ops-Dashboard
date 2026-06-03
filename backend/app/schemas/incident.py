from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "open"
    severity: Optional[str] = "medium"
    source: Optional[str] = None
    assigned_to: Optional[int] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    severity: Optional[str] = None
    assigned_to: Optional[int] = None

class IncidentOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    severity: str
    source: Optional[str] = None
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
