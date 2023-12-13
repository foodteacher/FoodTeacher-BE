from typing import Union
from fastapi import FastAPI

from app.db.session import db_engine
from app.db.base import Base

from fastapi.middleware.cors import CORSMiddleware

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