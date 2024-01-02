from pydantic import BaseModel

class UserBase(BaseModel):
    id: int

class UserCreate(UserBase):
    kakao_id: str

class KakaoCode(BaseModel):
    code: str

class UserSignup(BaseModel):
    name: str
    height: float
    weight: float
    age: int
    gender: str
    target_weight: float

class UserInput(BaseModel):
    query: str