from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_setting
from app.core.security import create_token
from app.db.session import get_db
from app.models.user_info import User
from app.schemas.user import UserUpdate
from app.schemas.token import Token, RefreshToken
from app.crud.v1.user import crud_user
from app.api.depends import get_current_user

import requests

router = APIRouter()
settings = get_setting()

@router.post("/refresh/jwt/access_token")
def get_jwt_access_token_by_refresh_token(refresh_token: RefreshToken, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Token:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(subject=current_user.kakao_id, expires_delta=access_token_expires)
    res = Token(access_token=access_token, refresh_token=refresh_token.token, token_type="bearer")
    return res

@router.post("/refresh/kakao/access_token")
def get_kakao_access_token_by_refresh_token(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _res = request_kakao_access_token(current_user, db)

    if _res.status_code != 200:
        raise HTTPException(status_code=401, detail="Kakao refresh token authentication failed")
    
    _result = _res.json()
    update_data_dict = {"kakao_access_token": _result["access_token"]}

    if "refresh_token" in _result:
        update_data_dict["kakao_refresh_token"] = _result["refresh_token"]

    update_data = UserUpdate(**update_data_dict)
    crud_user.update(db=db, db_obj=current_user, obj_in=update_data)
    return _result["access_token"]

def request_kakao_access_token(current_user: User, db: Session):
    REST_API_KEY = settings.KAKAO_REST_API_KEY
    
    _url = f'https://kauth.kakao.com/oauth/token'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "client_id": REST_API_KEY,
        "refresh_token": current_user.kakao_refresh_token,
    }
    return requests.post(_url, headers=headers, data=data)