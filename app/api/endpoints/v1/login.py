from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import get_setting
from app.core.security import get_jwt
from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.token import Token
from app.schemas.kakao import KakaoCode
from app.schemas.user_diet_plan_info import UserDietPlanInfoCreate
from app.schemas.exercise import ExerciseCreate
from app.schemas.menu import MenuCreate
from app.crud.v1.user import crud_user
from app.crud.v1.user_diet_plan_info import crud_user_diet_plan_info
from app.crud.v1.exercise import crud_exercise
from app.crud.v1.menu import crud_menu

import requests

router = APIRouter()
settings = get_setting()

# 엑세스 토큰을 저장할 변수
@router.post('/login')
async def kakaoAuth(authorization_code: KakaoCode, request: Request, db: Session = Depends(get_db)) -> Token:
    kakao_token = get_kakao_token(authorization_code=authorization_code, request=request)
    kakao_access_token = kakao_token.get("access_token")
    kakao_refresh_token = kakao_token.get("refresh_token")

    kakao_id = get_kakao_id(kakao_access_token)
    user = crud_user.get_by_kakao_id(db, kakao_id=kakao_id)
    jwt = get_jwt(db=db, kakao_id=kakao_id)
    if user:
        new_user = UserUpdate(kakao_access_token=kakao_access_token, kakao_refresh_token=kakao_refresh_token, jwt_refresh_token=jwt.refresh_token)
        crud_user.update(db=db, db_obj=user, obj_in=new_user)
        return jwt
    
    new_user = UserCreate(kakao_id=kakao_id, kakao_access_token=kakao_access_token, kakao_refresh_token=kakao_refresh_token, jwt_refresh_token=jwt.refresh_token)
    create_user(db=db, new_user=new_user)
    return jwt

def get_kakao_token(authorization_code: KakaoCode, request: Request):
    REST_API_KEY = settings.KAKAO_REST_API_KEY
    scheme = request.headers.get('x-forwarded-for')
    if scheme == '34.125.247.54':
        REDIRECT_URI = settings.REDIRECT_URI_PRODUCTION
    else:
        REDIRECT_URI = settings.REDIRECT_URI_DEVELOPMENT
    
    # REDIRECT_URI = settings.REDIRECT_URI_DEVELOPMENT
    _url = f'https://kauth.kakao.com/oauth/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "code": authorization_code.code,
        "redirect_uri": REDIRECT_URI
    }
    _res = requests.post(_url, headers=headers, data=data)
    
    if _res.status_code == 200:
        _result = _res.json()
        return _result
    else:
        raise HTTPException(status_code=401, detail="Kakao code authentication failed")

def get_kakao_id(kakao_access_token):
    _url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {kakao_access_token}"
    }
    _res = requests.get(_url, headers=headers)

    if _res.status_code == 200:
        response_data = _res.json()
        user_id = response_data.get("id")
        return user_id
    else:
        raise HTTPException(status_code=401, detail="Kakao access token authentication failed")

def create_user(*, db: Session, new_user: UserCreate):
    user = crud_user.create(db, obj_in=new_user)

    new_user_diet_plan_info = UserDietPlanInfoCreate(user_id=user.id)
    user_diet_plan_info = crud_user_diet_plan_info.create(db=db, obj_in=new_user_diet_plan_info)

    new_exercise = ExerciseCreate(user_diet_plan_info_id=user_diet_plan_info.id)
    crud_exercise.create(db=db, obj_in=new_exercise)

    meal_times = ["breakfast", "lunch", "dinner"]
    create_menu(db=db, meal_times=meal_times, user_diet_plan_info_id=user_diet_plan_info.id)
    return user

def create_menu(*, db: Session, meal_times: List, user_diet_plan_info_id: int):
    for meal_time in meal_times:
        new_menu = MenuCreate(user_diet_plan_info_id=user_diet_plan_info_id, meal_time=meal_time)
        crud_menu.create(db,obj_in=new_menu)
    return