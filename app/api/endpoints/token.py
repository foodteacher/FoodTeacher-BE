from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.core.config import get_setting
from app.core.security import create_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.token import Token, RefreshToken
from app.schemas.kakao import KakaoId, KakaoCode
from app.crud.user import crud_user
from app.api.depends import get_current_user
from fastapi_sessions import session_verifier

import requests

router = APIRouter()
settings = get_setting()

@router.post("/refresh/jwt/access-token")
def get_jwt_access_token_by_refresh_token(refresh_token: RefreshToken, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Token:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(subject=current_user.kakao_id, expires_delta=access_token_expires)
    res = Token(access_token=access_token, refresh_token=refresh_token.token, token_type="bearer")
    return res

@router.post("/refresh/kakao/access-token")
def get_kakao_access_token_by_refresh_token(kakao_id: KakaoId, db: Session = Depends(get_db)):
    REST_API_KEY = settings.REST_API_KEY
    id = kakao_id.id
    current_user = crud_user.get_by_kakao_id(db=db, kakao_id=id)
    
    _url = f'https://kauth.kakao.com/oauth/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": REST_API_KEY,
        "refresh_token": current_user.kakao_refresh_token,
    }
    _res = requests.post(_url, headers=headers, data=data)

    if _res.status_code == 200:
        _result = _res.json()
        if "refresh_token" in _result:
            refresh_token = _result["refresh_token"]
            obj_in = UserUpdate(kakao_refresh_token=refresh_token)
            crud_user.update(db=db, db_obj=current_user, obj_in=obj_in)
        return _result["access_token"]
    else:
        raise HTTPException(status_code=401, detail="Kakao code authentication failed")