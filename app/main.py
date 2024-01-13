from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router

from .db.session import Base, engine
# service
from .service.foodteacher import calculate_calory

import json

# app 생성
def create_tables():
    Base.metadata.create_all(bind=engine)

def get_application():
    app = FastAPI()
    create_tables()
    return app

app = get_application()

origins = [
    "http://localhost:3000",
    "https://www.foodteacher.xyz"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용하려면 "*"
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용하려면 "*"
)

app.include_router(api_router)

@app.get("/")
def read_root():
    # res = calculate_calory("아침은 사과를 먹었고, 점심은 바나나, 저녁은 마라탕 먹었어.", 2000)
    # _res = json.loads(res)
    # print(_res)
    return "hello, 팩트폭행단~!"