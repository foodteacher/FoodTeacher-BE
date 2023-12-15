from pydantic import BaseModel

class UserBaseModel(BaseModel):
    name: str
    height: float
    weight: float
    age: int
    gender: str
    targetWeight: float

class UserInput(BaseModel):
    query: str