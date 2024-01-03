from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    id: int

class UserCreate(UserBase):
    kakao_id: str

class UserSignup(UserCreate):
    name: str
    height: float
    weight: float
    age: int
    gender: str
    target_weight: float

class UserUpdate(UserBase):
    username: Optional[str] = None

class KakaoCode(BaseModel):
    code: str

class UserInput(BaseModel):
    query: str

class UserInDBBase(UserBase):
    kakao_id: str
    name: str
    height: float
    weight: float
    age: int
    gender: str
    target_weight: float

    class Config:
        from_attributes = True


class UserRead(UserInDBBase):
    pass