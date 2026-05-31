from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class LogBase(BaseModel):
    timestamp: datetime
    level: str
    message: str
    source: Optional[str] = None
    incident_id: Optional[int] = None

class LogCreate(LogBase):
    pass

class LogOut(LogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True