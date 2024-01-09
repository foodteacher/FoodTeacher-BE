from pydantic import BaseModel

class UserDietPlanInfoBase(BaseModel):
    user_id: int

class UserDietPlanInfoCreate(UserDietPlanInfoBase):
    pass

class UserDietPlanInfoInDBBase(UserDietPlanInfoBase):
    class Config:
        from_attributes = True
        
class UserDietPlanInfoRead(UserDietPlanInfoInDBBase):
    pass

class UserDietPlanInfoUpdate(UserDietPlanInfoBase):
    pass