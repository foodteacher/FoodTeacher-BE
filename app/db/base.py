from .base_class import Base
from .models.dietPlanMenu import DietPlanMenu
from .models.menu import Menu
from .models.user import User
from .models.userDietPlan import UserDietPlan
from sqlalchemy.exc import OperationalError

from sqlalchemy.orm import Session

from ..schemas import user

def user_save_access_token(db: Session, access_token: str):
    user = User(kakao_token=access_token)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def user_save_kakao_id(db: Session, new_kakao_id: str, kakao_token: str):
    user = db.query(User).filter(User.kakao_token == kakao_token).first()

    if user:
        user.kakao_id = new_kakao_id
        db.commit()
        db.refresh(user)
    else:
        pass

    return user

async def get_user_by_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.userId == user_id).first()

async def get_user_by_user_id_retry(db: Session, user_id: int, max_retries: int = 3, current_retry: int = 0):
    try:
        return db.query(User).filter(User.userId == user_id).first()
    except OperationalError as e:
        if current_retry < max_retries:
            # 재시도 횟수가 최대 횟수 미만일 때 재귀적으로 호출
            return await get_user_by_user_id_retry(db, user_id, max_retries, current_retry + 1)
        else:
            # 최대 재시도 횟수를 초과하면 예외를 다시 발생시킴
            raise e

async def get_user_by_kakao_id(db: Session, kakao_id: int):
    return db.query(User).filter(User.kakao_id == kakao_id).first()

async def user_create(user_data: user.UserCreateModel, db: Session):
    user = User(
        name = user_data.name,
        height = user_data.height,
        weight = user_data.weight,
        age = user_data.age,
        gender = user_data.gender,
        targetWeight = user_data.targetWeight
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_users(db: Session):
    return db.query(User).all()

def delete_all_users(db: Session):
    db.query(User).delete()
    db.commit()