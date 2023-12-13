from typing import Union
from fastapi import FastAPI

from app.db.session import db_engine
from app.db.base import Base

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session  # 데이터베이스 세션을 사용하기 위해 추가
from app.db.session import SessionLocal  # SessionLocal을 가져옴

from app.utils import UserCreate, UserResponse
from app.db.models.user import User

def create_tables():
    Base.metadata.create_all(bind=db_engine)

def get_application():
    app = FastAPI()
    create_tables()
    return app

app = get_application()

# CORS 설정
origins = [
    "*"  # 원하는 도메인 및 포트를 추가
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
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# FastAPI 앱이 시작될 때 데이터베이스 연결
@app.on_event("startup")
async def startup_db_client():
    print("서버 연결됨!!")

# FastAPI 앱이 종료될 때 데이터베이스 연결 해제
@app.on_event("shutdown")
async def shutdown_db_client():
    print("서버 연결 해제!!")

# @app.post("/users/", response_model=UserResponse)
# def register_user(user_input: UserCreate):
#     # 네이버 클로바 API를 사용하여 기초 대사량 얻기
#     basal_metabolic_rate = get_basal_metabolic_rate(
#         user_input.height, user_input.weight, user_input.age, user_input.gender
#     )

#     # 사용자 정보와 기초 대사량을 데이터베이스에 저장
#     db = SessionLocal()
#     user_data = user_input.dict()
#     user_data["basalMetabolicRate"] = basal_metabolic_rate
#     user = create_user(db, user_data)

#     return user
