from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MenuBase(BaseModel):
    user_diet_plan_info_id: Optional[int] = None
    name: Optional[str] = None
    calories: Optional[float] = None
    meal_time: Optional[str] = None
    created_at: Optional[datetime] = None

    10_10_10-32-12

class MenuCreate(MenuBase):
    pass

class MenuInDBBase(MenuBase):
    class Config:
        from_attributes = True
        
class MenuRead(MenuInDBBase):
    pass

class MenuUpdate(MenuBase):
    pass