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

# 모델을 사용하여 반환할 데이터 정의
class CreateUserResponse(BaseModel):
    user: dict  # user 정보
    JWT: str    # JWT 토큰