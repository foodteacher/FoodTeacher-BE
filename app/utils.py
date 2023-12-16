from pydantic import BaseModel

class UserBaseModel(BaseModel):
    name: str
    kakao_token: str
    kakao_id: str
    height: float
    weight: float
    age: int
    gender: str
    targetWeight: float

class UserInput(BaseModel):
    query: str

class KakaoCode(BaseModel):
    code: str

class UserCreateModel(BaseModel):
    name: str
    height: float
    weight: float
    age: int
    gender: str
    targetweight: float