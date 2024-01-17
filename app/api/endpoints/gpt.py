from fastapi import APIRouter, Depends
import json
from json import JSONDecodeError

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.gpt import UserQuery
from app.api.depends import get_current_user
from app.schemas.exercise import ExerciseUpdate
from app.schemas.menu import MenuUpdate
from app.crud.user import crud_user
from app.crud.userDietPlanInfo import crud_user_diet_plan_info
from app.crud.exercise import crud_exercise
from app.crud.menu import crud_menu

from app.service.foodteacher import calculate_calory, calculate_bmr


router = APIRouter()

@router.post("/diet-exercise-advice")
def get_answer_from_gpt(query: UserQuery, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bmr = calculate_bmr(current_user)
    res = calculate_calory(query.query, bmr)
    try:
        result = json.loads(res)
    except JSONDecodeError as e:
        print(f"Error json.loads: {e}")
    
    update_user_diet_plan_info(db, result, current_user.id)
    return result

def update_user_diet_plan_info(db: Session, result: dict, user_id: int):
    user_diet_plan_info = crud_user_diet_plan_info.get_by_user_id(db=db, user_id=user_id)
    
    menus = crud_menu.get_by_user_diet_plan_info(db=db, user_diet_plan_info_id=user_diet_plan_info.id)
    for menu in menus:
        try:
            meal_time_ = menu.meal_time
            meal_time_data = result.get(meal_time_)
            obj_in = MenuUpdate(name=meal_time_data.get("menu", ""), calories=meal_time_data.get("calories", 0))
            crud_menu.update(db=db, db_obj=menu, obj_in=obj_in)
        except (KeyError, TypeError) as e:
            print(f"Error updating menu: {e}")
    
    exercise = crud_exercise.get_by_user_diet_plan_info(db=db, user_diet_plan_info_id=user_diet_plan_info.id)
    try:
        advice = result.get("잔소리", "")
        recommended_exercise = result.get("운동필요시간", "")
        excess_calories = result.get("초과칼로리", 0)
        obj_in = ExerciseUpdate(advice=advice, recommended_exercise=recommended_exercise, excess_calories=excess_calories)
        crud_exercise.update(db=db, db_obj=exercise, obj_in=obj_in)
    except (KeyError, TypeError) as e:
        print(f"Error updating exercise: {e}")

    return
