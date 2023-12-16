# fastapi
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Optional
import requests
import json
# JWT
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
# db
from app.db.session import db_engine
from app.db.base import Base
from sqlalchemy.orm import Session  # 데이터베이스 세션을 사용하기 위해 추가
from app.db.session import get_db, SessionLocal  # SessionLocal을 가져옴
from .db import base
# python 데이터 모델
from . import utils
# service
from .service.clova_ai import get_executor
from .service.bmr_calculator import calculate_bmr
from .service.food_teacher import get_diet_exercise_advice
#security
from app.security.jwt import get_current_user, get_jwt
from fastapi.security import OAuth2PasswordRequestForm

# app 생성
def create_tables():
    Base.metadata.create_all(bind=db_engine)

def get_application():
    app = FastAPI()
    create_tables()
    return app

app = get_application()

# CORS 설정
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:3000",  # 원하는 도메인 및 포트를 추가
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

############################################# 임시 api ####################################
@app.get("/del")
def del_db_table(db: Session = Depends(get_db)):
    base.delete_all_users(db)
    return "good"

@app.get("/temp")
def temp_endpoint():
    db = SessionLocal()
    user_data = utils.UserBaseModel(
        name="서경원",
        kakao_token="fdkajklajfdskl223123kfjsklfj3",
        kakao_id="fjksdalf",
        height=173,
        weight=72,
        age=29,
        gender="male",
        targetWeight=65.0    
    )
    result = base.user_create(db, user_data)
    db.commit()
    db.close()
    return result

############################################# kakao api ####################################
# 엑세스 토큰을 저장할 변수
@app.post('/auth')
async def kakaoAuth(code: utils.KakaoCode, db: Session = Depends(get_db)):
    REST_API_KEY = '536cb646ce60d71102dc92d2b7845c8d'
    # REDIRECT_URI = 'http://fe-fe-544a1-21216457-67a2ef796b03.kr.lb.naverncp.com/signup'
    REDIRECT_URI = "http://localhost:3000/signup"
    _url = f'https://kauth.kakao.com/oauth/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "code": code.code,
        "redirect_uri": REDIRECT_URI
    }
    _res = requests.post(_url, headers=headers, data=data) 
    _result = _res.json()
    access_token = _result.get("access_token")

    base.user_save_access_token(db, access_token)

    _url = "https://kapi.kakao.com/v2/user/me"
    kakao_user_id = get_kakao_user_id(_url, access_token)
    jwt = get_jwt(kakao_user_id)

    return {"jwt": jwt, "token_type": "bearer"}

def get_kakao_user_id(_url, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    _res = requests.get(_url, headers=headers)

    if _res.status_code == 200:
        response_data = _res.json()
        user_id = response_data.get("id")
        return user_id
    else:
        raise HTTPException(status_code=401, detail="Kakao authentication failed")

############################################# 유저 관련 api ####################################
@app.post("/users/")
def create_user(user_data: utils.UserBaseModel, db: Session = Depends(get_db)):
    return base.user_create(db=db, user_data=user_data)

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = base.users_read(db)
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = base.user_read(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users")
def delete_users(db: Session = Depends(get_db)):
    base.delete_all_users(db)
    return {"message": "All users deleted"}

@app.get("/users/{user_id}/bmr")
def read_user_bmr(user_id: int, db: Session = Depends(get_db)):
    user = base.user_read(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"bmr": calculate_bmr(user)}

@app.post("/users/{user_id}/diet-exercise-advice")
def get_answer_from_clova(user_id: int, user_input: utils.UserInput, db: Session = Depends(get_db)):
    executor = get_executor()
    user = base.user_read(db, user_id)
    bmr = calculate_bmr(user)

    result = get_diet_exercise_advice(executor, bmr, user_input.query)
    data = json.loads(result)

    if "error" in data:
        raise HTTPException(status_code=404, detail="error has been occured")
    return data