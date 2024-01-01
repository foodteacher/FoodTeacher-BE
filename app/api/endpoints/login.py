from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_setting
from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.user import UserCreate
from app.crud.user import crud_user

router = APIRouter()
settings = get_setting()

@router.post("/register")
def post(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud_user.create(db=db, obj_in=user)


@router.post("/login/access-token")
async def login_for_access_token(user: UserCreate, db: Session = Depends(get_db)):
    user = crud_user.authenticate(db=db, username=user.username, password=user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.username, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
