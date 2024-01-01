from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from app.api.depends import get_current_active_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserBase, UserCreate
from app.api.depends import get_db
from sqlalchemy.orm import Session
from app.crud.user import crud_user

router = APIRouter()

@router.get("/me", response_model=UserRead, response_model_exclude={"password"})
def read_user_me(current_user: User = Depends(get_current_active_user)) -> UserRead:
    print(current_user)
    return current_user

@router.patch('/me', response_model=UserRead, response_model_exclude={"password"})
def update_user_me(*, db: Session = Depends(get_db), password: str = Body(None), username: str = Body(None), current_user: User = Depends(get_current_active_user)):
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password:
        user_in.password = password
    else:
        del user_in.password
    if username:
        user_has_same_username = crud_user.get_by_username(db=db, username=username)
        if user_has_same_username:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            user_in.username = username
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user