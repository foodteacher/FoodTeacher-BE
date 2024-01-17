from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.api.depends import get_db
from app.api.depends import get_current_user
from app.core.security import get_jwt
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserInfo
from app.crud.menu import crud_menu
from app.crud.userDietPlanInfo import crud_user_diet_plan_info
from app.crud.exercise import crud_exercise
from app.crud.user import crud_user

router = APIRouter()

@router.get("/me", response_model=Optional[UserRead], response_model_exclude={"kakao_access_token": True, "kakao_refresh_token": True, "jwt_refresh_token": True})
def read_user_me(current_user: Optional[User] = Depends(get_current_user)) -> Optional[UserRead]:
    return current_user

@router.patch('/register', response_model=UserRead, response_model_exclude={"kakao_access_token": True, "kakao_refresh_token": True, "jwt_refresh_token": True})
def register_user(*, db: Session = Depends(get_db), new_user_data: UserUpdate, current_user: User = Depends(get_current_user)) -> UserRead:
    user = crud_user.update(db, db_obj=current_user, obj_in=new_user_data)
    return user

@router.get("/me/mypage", response_model=UserInfo)
def get_info(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> UserInfo:
    user_diet_plan_info = crud_user_diet_plan_info.get_by_user_id(db=db, user_id=current_user.id)
    menus = crud_menu.get_by_user_diet_plan_info(db=db, user_diet_plan_info_id=user_diet_plan_info.id)
    exercise = crud_exercise.get_by_user_diet_plan_info(db=db, user_diet_plan_info_id=user_diet_plan_info.id)
    user_info_dic = {
        "name": current_user.name,
        "gender": current_user.gender,
        "age": current_user.age,
        "height": current_user.height,
        "weight": current_user.weight,
        "target_weight": current_user.target_weight,
        "advice": exercise.advice,
        "recommended_exercise": exercise.recommended_exercise,
        "excess_calories": exercise.excess_calories,
    }
    for menu in menus:
        user_info_dic[menu.meal_time] = {"menu": menu.name, "calories": menu.calories}
    
    return UserInfo(**user_info_dic)
    