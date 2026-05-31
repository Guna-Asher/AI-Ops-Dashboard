from typing import Any, Optional
from pydantic import BaseModel

class WidgetBase(BaseModel):
    name: str
    widget_type: str
    config: Optional[Any] = None

class WidgetCreate(WidgetBase):
    pass

class WidgetOut(WidgetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True