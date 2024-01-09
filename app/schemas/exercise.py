from pydantic import BaseModel

class ExerciseBase(BaseModel):
    user_diet_plan_info_id: int = None
    advice: str = None
    recommended_exercise: str = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseInDBBase(ExerciseBase):
    class Config:
        from_attributes = True
        
class ExerciseRead(ExerciseInDBBase):
    pass

class ExerciseUpdate(ExerciseBase):
    pass