from typing import Union
from fastapi import FastAPI, Depends, HTTPException

from app.db.session import db_engine
from app.db.base import Base

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session  # 데이터베이스 세션을 사용하기 위해 추가
from app.db.session import get_db, SessionLocal  # SessionLocal을 가져옴

from . import utils
from .db import base

from .service.bmr_calculator import calculate_bmr

def create_tables():
    Base.metadata.create_all(bind=db_engine)

def get_application():
    app = FastAPI()
    create_tables()
    return app

app = get_application()

# CORS 설정
origins = [
    "http://localhost:3000",  # 원하는 도메인 및 포트를 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용하려면 "*"
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용하려면 "*"
)

@app.get("/")
def read_root():
    return "hello, 팩트폭행단~!"

@app.get("/temp")
def temp_endpoint():
    db = SessionLocal()
    user_data = utils.UserBaseModel(
        name="서경원",
        height=173,
        weight=72,
        age=29,
        gender="male",
        targetWeight=65.0   
    )
    result = base.user_create(db, user_data)
    db.close()
    return result

@app.post("/users/")
def create_user(user_data: utils.UserBaseModel, db: Session = Depends(get_db)):
    return base.user_create(db=db, user_data=user_data)

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = base.users_read(db)
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = base.user_read(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users")
def delete_users(db: Session = Depends(get_db)):
    base.delete_all_users(db)
    return {"message": "All users deleted"}

@app.get("/users/{user_id}/bmr")
def read_user_bmr(user_id: int, db: Session = Depends(get_db)):
    user = base.user_read(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"bmr": calculate_bmr(user)}
