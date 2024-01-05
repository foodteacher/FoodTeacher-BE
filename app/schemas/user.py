from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    id: Optional[int] = None

class UserCreate(UserBase):
    kakao_id: int

class UserUpdate(UserBase):
    name: str = None
    height: float = None
    weight: float = None
    age: int = None
    gender: str = None
    target_weight: float = None
    refresh_token: str = None

class KakaoCode(BaseModel):
    code: str

class UserInput(BaseModel):
    query: str

class UserInDBBase(UserBase):
    kakao_id: int
    name: str
    height: float
    weight: float
    age: int
    gender: str
    target_weight: float
    refresh_token: str

    class Config:
        from_attributes = True


class UserRead(UserInDBBase):
    pass