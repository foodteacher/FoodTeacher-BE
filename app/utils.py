from pydantic import BaseModel

class UserBaseModel(BaseModel):
    name: str
    kakao_token: str
    height: float
    weight: float
    age: int
    gender: str
    targetWeight: float

class UserInput(BaseModel):
    query: str

class KakaoCode(BaseModel):
    code: str