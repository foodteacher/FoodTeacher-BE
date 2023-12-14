from typing import Union
from fastapi import FastAPI, Depends

from app.db.session import db_engine
from app.db.base import Base

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session  # 데이터베이스 세션을 사용하기 위해 추가
from app.db.session import get_db, SessionLocal  # SessionLocal을 가져옴

from . import utils
from .db import base

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

@app.post("/users/")
def create_user(user_data: utils.UserBaseModel, db: Session = Depends(get_db)):
    return base.user_create(db=db, user_data=user_data)

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = base.user_read(db)
    return users

