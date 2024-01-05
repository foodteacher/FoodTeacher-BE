import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import get_setting
from app.db.session import SessionLocal
from app.models.user import User
from app.crud.user import crud_user
from app.schemas.token import TokenPayload
from datetime import datetime

from app.db.session import get_db

from app.core.session import verifier

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/")
settings = get_setting()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud_user.get_by_kakao_id(db, kakao_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    exp = token_data.exp
    if datetime.fromtimestamp(exp) > datetime.now():
        return user
    else:
        raise HTTPException(
            status_code=401,
            detail="Access token is expired. Please request access token"
        )
    
def validate_refresh_token(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = crud_user.get_by_kakao_id(db, kakao_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    exp = token_data.exp
    if datetime.fromtimestamp(exp) < datetime.now():
        return False
    return True