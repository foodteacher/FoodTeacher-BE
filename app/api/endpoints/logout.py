from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.core.config import get_setting
from app.api.depends import get_current_user
from app.crud.user import crud_user
from app.models.user import User

import requests


router = APIRouter()
settings = get_setting()

@router.post('/logout')
def logout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    kakao_logout(current_user=current_user)
    res = crud_user.remove_field(db=db, db_obj=current_user, field="refresh_token")
    return res

def kakao_logout(current_user: User):
    access_token = current_user.kakao_access_token
    _url = f"https://kapi.kakao.com/v1/user/logout"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
    }
    _res = requests.post(_url, headers=headers)
    
    if _res.status_code == 200:
        _result = _res.json()
        return _result
    else:
        raise HTTPException(status_code=401, detail="Kakao logout failed")