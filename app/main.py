# fastapi
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Optional
import requests
import json
# service
from .service.clova_ai import get_executor
from .service.bmr_calculator import calculate_bmr
from .service.food_teacher import get_diet_exercise_advice
from .db.session import Base, engine


# app 생성
def create_tables():
    Base.metadata.create_all(bind=engine)

def get_application():
    app = FastAPI()
    create_tables()
    return app

app = get_application()

# CORS 설정
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:3000",
    "http://be-be-c957f-21216619-aeb7ba37580c.kr.lb.naverncp.com",
    "http://ing-fe-redirectingress-b09e0-21395882-5398597ca2af.kr.lb.naverncp.com"
    "http://www.foodteacher.xyz/",
    "https://www.foodteacher.xyz/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용하려면 "*"
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용하려면 "*"
)

@app.get("/")
def read_root():
    return "hello, 팩트폭행단~!"

############################################# kakao api ####################################
# # 엑세스 토큰을 저장할 변수
# @app.post('/auth')
# async def kakaoAuth(code: utils.KakaoCode, db: Session = Depends(get_db)):
#     REST_API_KEY = '536cb646ce60d71102dc92d2b7845c8d'
#     # REDIRECT_URI = 'http://fe-fe-544a1-21216457-67a2ef796b03.kr.lb.naverncp.com/signup'
#     REDIRECT_URI = "http://localhost:3000/signup"
#     _url = f'https://kauth.kakao.com/oauth/token'
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {
#         "grant_type": "authorization_code",
#         "client_id": REST_API_KEY,
#         "code": code.code,
#         "redirect_uri": REDIRECT_URI
#     }
#     _res = requests.post(_url, headers=headers, data=data) 
#     _result = _res.json()
#     access_token = _result.get("access_token")

#     base.user_save_access_token(db, access_token)

#     _url = "https://kapi.kakao.com/v2/user/me"
#     kakao_user_id = get_kakao_user_id(_url, access_token)
#     user = base.get_user_by_kakao_id(db, kakao_id=kakao_user_id)
#     if user:
#         return {"user_id": user.userId}
#     user = base.user_save_kakao_id(db, kakao_user_id, access_token)
#     # jwt = get_jwt(kakao_user_id)

#     return {"new_user_id": user.userId}

# def get_kakao_user_id(_url, access_token):
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
#     _res = requests.get(_url, headers=headers)

#     if _res.status_code == 200:
#         response_data = _res.json()
#         user_id = response_data.get("id")
#         return user_id
#     else:
#         raise HTTPException(status_code=401, detail="Kakao authentication failed")

############################################# 유저 관련 api ###########################################    
# @app.post("/users")
# async def create_user(user_data: user.UserCreateModel, db: Session = Depends(get_db)):
#     user = await base.user_create(db=db, user_data=user_data)
#     return {"user_id": user.userId}

# @app.get("/users/{user_id}")
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     user = base.get_user_by_user_id(db, user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @app.delete("/users")
# def delete_users(db: Session = Depends(get_db)):
#     base.delete_all_users(db)
#     return {"message": "All users deleted"}

# @app.get("/users/{user_id}/bmr")
# def read_user_bmr(user_id: int, db: Session = Depends(get_db)):
#     user = base.user_read(db, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"bmr": calculate_bmr(user)}

# @app.post("/users/{user_id}/diet-exercise-advice")
# async def get_answer_from_clova(user_id: int, user_input: user.UserInput, db: Session = Depends(get_db)):
#     executor = get_executor()
#     user = await base.get_user_by_user_id(db, user_id)
#     bmr = calculate_bmr(user)

#     result = get_diet_exercise_advice(executor, bmr, user_input.query)
#     print(result)
#     data = json.loads(result)

#     if "error" in data:
#         raise HTTPException(status_code=404, detail="error has been occured")
#     return data

# @app.post("/users/diet-exercise-advice")
# async def get_answer_from_clova(user_input: user.TempUserInput, db: Session = Depends(get_db)):
#     executor = get_executor()
#     bmr = calculate_bmr(user_input)

#     result = get_diet_exercise_advice(executor, bmr, user_input.query)
#     print(result)
#     data = json.loads(result)

#     if "error" in data:
#         raise HTTPException(status_code=404, detail="error has been occured")
#     return data
