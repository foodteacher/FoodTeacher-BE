from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    password: str
    height: float
    weight: float
    age: int
    gender: str
    targetWeight: float

class UserResponse(BaseModel):
    userId: int
    name: str
    height: float
    weight: float
    age: int
    gender: str
    targetWeight: float
    basalMetabolicRate: float