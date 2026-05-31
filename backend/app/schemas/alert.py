from typing import Optional
from pydantic import BaseModel

class AlertBase(BaseModel):
    name: str
    condition: str
    action: str
    enabled: bool = True

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    name: Optional[str] = None
    condition: Optional[str] = None
    action: Optional[str] = None
    enabled: Optional[bool] = None

class AlertOut(AlertBase):
    id: int
    created_by: Optional[int] = None
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True