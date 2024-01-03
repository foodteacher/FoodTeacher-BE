from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_setting
from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.user import KakaoCode, UserCreate
from app.schemas.token import Token
from app.crud.user import crud_user

import requests

router = APIRouter()
settings = get_setting()

# @router.post("/register")
# def post(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = crud_user.get_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="username already registered")
#     return crud_user.create(db=db, obj_in=user)


# @router.post("/login/access-token")
# async def login_for_access_token(user: UserCreate, db: Session = Depends(get_db)):
#     user = crud_user.authenticate(db=db, username=user.username, password=user.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(subject=user.username, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}

# 엑세스 토큰을 저장할 변수
@router.post('/login')
async def kakaoAuth(authorization_code: KakaoCode, db: Session = Depends(get_db)):
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
        "code": authorization_code.code,
        "redirect_uri": REDIRECT_URI
    }
    _res = requests.post(_url, headers=headers, data=data) 
    _result = _res.json()
    kakao_access_token = _result.get("access_token")
    kakao_refresh_token = _result.get("refresh_token")

    _url = "https://kapi.kakao.com/v2/user/me"
    kakao_id = get_kakao_id(_url, kakao_access_token)

    user = crud_user.get_by_kakao_id(db, kakao_id=kakao_id)
    if user:
        return {"user_id": user.id}
    
    obj_in = UserCreate(kakao_id=kakao_id)
    user = crud_user.create(db, obj_in=obj_in)

    jwt = get_jwt(db=db, obj_in=obj_in)

    return jwt

def get_kakao_id(_url, kakao_access_token):
    headers = {
        "Authorization": f"Bearer {kakao_access_token}"
    }
    _res = requests.get(_url, headers=headers)

    if _res.status_code == 200:
        response_data = _res.json()
        user_id = response_data.get("id")
        return user_id
    else:
        raise HTTPException(status_code=401, detail="Kakao authentication failed")
    
def get_jwt(*, obj_in: UserCreate, db: Session = Depends(get_db)):
    user = crud_user.get_by_kakao_id(db, kakao_id=obj_in.kakao_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail="Incorrect username or password",
            detail="Incorrect kakao_id",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.kakao_id, expires_delta=access_token_expires)
    
    res = Token(access_token=access_token, token_type="bearer")
    return res