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

import requests

# def get_basal_metabolic_rate(height: float, weight: float, age: int, gender: str):
#     # 네이버 클로바 API 요청
#     api_url = "https://api.clova.ai/your/basal_metabolic_rate/api/endpoint"
#     payload = {
#         "height": height,
#         "weight": weight,
#         "age": age,
#         "gender": gender,
#     }
#     response = requests.post(api_url, json=payload)

#     # API 응답 처리
#     if response.status_code == 200:
#         data = response.json()
#         basal_metabolic_rate = data["basal_metabolic_rate"]
#         return basal_metabolic_rate
#     else:
#         # API 호출 실패 시 예외 처리
#         raise Exception("네이버 클로바 API 호출 실패")
