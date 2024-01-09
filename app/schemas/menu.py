from pydantic import BaseModel
from datetime import datetime

class MenuBase(BaseModel):
    user_diet_plan_info_id: int
    name: str = None
    calories: float = None
    meal_time: str
    created_at: datetime = None

class MenuCreate(MenuBase):
    pass

class MenuInDBBase(MenuBase):
    class Config:
        from_attributes = True
        
class MenuRead(MenuInDBBase):
    pass

class MenuUpdate(MenuBase):
    pass