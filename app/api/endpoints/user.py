from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from app.api.depends import get_current_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserRegist
from app.api.depends import get_db
from sqlalchemy.orm import Session
from app.crud.user import crud_user

router = APIRouter()

@router.get("/me", response_model=UserRead)
def read_user_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user

@router.patch('/register', response_model=UserRead)
def register_user(*, db: Session = Depends(get_db), new_user_data: UserRegist = Body(None), current_user: User = Depends(get_current_user)):
    current_user_data = current_user
    user = crud_user.regist(db, db_obj=current_user_data, obj_in=new_user_data)
    return user