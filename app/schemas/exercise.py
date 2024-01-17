from pydantic import BaseModel
from typing import Optional

class ExerciseBase(BaseModel):
    user_diet_plan_info_id: Optional[int] = None
    advice: Optional[str] = None
    recommended_exercise: Optional[str] = None
    excess_calories: Optional[float] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseInDBBase(ExerciseBase):
    class Config:
        from_attributes = True
        
class ExerciseRead(ExerciseInDBBase):
    pass

class ExerciseUpdate(ExerciseBase):
    pass