from typing import Any

from fastapi import APIRouter, Depends

from app.api.depends import get_current_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.api.depends import get_db
from sqlalchemy.orm import Session
from app.crud.user import crud_user

router = APIRouter()

@router.get("/me", response_model=UserRead, response_model_exclude={"kakao_access_token": True, "kakao_refresh_token": True, "jwt_refresh_token": True})
def read_user_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user

@router.patch('/register', response_model=UserRead, response_model_exclude={"kakao_access_token": True, "kakao_refresh_token": True, "jwt_refresh_token": True})
def register_user(*, db: Session = Depends(get_db), new_user_data: UserUpdate, current_user: User = Depends(get_current_user)) -> UserRead:
    user = crud_user.update(db, db_obj=current_user, obj_in=new_user_data)
    return user