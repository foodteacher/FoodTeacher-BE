from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router

from .db.session import Base, engine
# service
from .service.clova_ai import get_executor
from .service.bmr_calculator import calculate_bmr
from .service.food_teacher import get_diet_exercise_advice



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
    "http://be-be-c957f-21216619-aeb7ba37580c.kr.lb.naverncp.com",
    "http://ing-fe-redirectingress-b09e0-21395882-5398597ca2af.kr.lb.naverncp.com"
    "http://www.foodteacher.xyz/",
    "https://www.foodteacher.xyz/"
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
    return "hello, 팩트폭행단~!"

############################################# 서비스 관련 api ###########################################    
# @app.post("/users/{user_id}/diet-exercise-advice")
# async def get_answer_from_clova(user_id: int, user_input: user.UserInput, db: Session = Depends(get_db)):
#     executor = get_executor()
#     user = await base.get_user_by_user_id(db, user_id)
#     bmr = calculate_bmr(user)

#     result = get_diet_exercise_advice(executor, bmr, user_input.query)
#     print(result)
#     data = json.loads(result)

#     if "error" in data:
#         raise HTTPException(status_code=404, detail="error has been occured")
#     return data

# @app.post("/users/diet-exercise-advice")
# async def get_answer_from_clova(user_input: user.TempUserInput, db: Session = Depends(get_db)):
#     executor = get_executor()
#     bmr = calculate_bmr(user_input)

#     result = get_diet_exercise_advice(executor, bmr, user_input.query)
#     print(result)
#     data = json.loads(result)

#     if "error" in data:
#         raise HTTPException(status_code=404, detail="error has been occured")
#     return data