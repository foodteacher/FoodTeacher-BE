from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.core.config import get_setting
from app.api.depends import get_current_user
from app.crud.user import crud_user


router = APIRouter()
settings = get_setting()

@router.post('/')
def logout(refresh_token: str = Body(...),  db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    res = crud_user.remove_field(db=db, db_obj=current_user, field=refresh_token)
    return res