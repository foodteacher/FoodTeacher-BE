# security/jwt.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from ..db import base

from ..core.config import get_setting

settings = get_setting()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta = None):
    global SECRET_KEY, ALGORITHM
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_jwt(user_id):
    global ACCESS_TOKEN_EXPIRE_MINUTES
    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user_id}
    access_token = create_access_token(token_data, expires_delta=access_token_expires)
    return access_token

# JWT 토큰 검증 함수
def verify_token(token: str):
    global SECRET_KEY, ALGORITHM
    try:
        print("#######")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("$$$$$$$$$$$$$$$$$")
        user_id: str = payload.get("sub")
        print("*******************")
        exp_time = payload.get("exp")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if user_id is None:
            return None, None
        
        token_data = TokenData(user_id=user_id) 
    except JWTError:
        return None, None
    return token_data, exp_time

# JWT 토큰을 사용하여 사용자 확인 함수
async def get_current_user(token: str):
    global ACCESS_TOKEN_EXPIRE_MINUTES
    # 토큰 디코딩 및 사용자 확인 로직 작성
    token_data, exp_time = verify_token(token)
    print(token_data)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 토큰의 만료 시간 확인
    current_time = datetime.utcnow()
    if current_time > exp_time:
        # 토큰이 만료되었을 경우, 새로운 토큰 발급
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_token_data = {"sub": token_data.user_id}
        new_access_token = create_access_token(new_token_data, expires_delta=access_token_expires)
        return get_current_user(new_access_token)
    
    user = base.get_user_by_user_id(user_id=token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user, token

class TokenData(BaseModel):
    user_id: str