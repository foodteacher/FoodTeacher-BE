from pydantic import BaseModel

class UserBaseModel(BaseModel):
    name: str
    height: float
    weight: float
    age: int
    gender: str
    targetWeight: float

# class UserResponse(BaseModel):
#     userId: int
#     name: str
#     height: float
#     weight: float
#     age: int
#     gender: str
#     targetWeight: float
#     basalMetabolicRate: float