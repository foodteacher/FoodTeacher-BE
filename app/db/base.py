from .base_class import Base
from .models.dietPlanMenu import DietPlanMenu
from .models.menu import Menu
from .models.user import User
from .models.userDietPlan import UserDietPlan

from sqlalchemy.orm import Session

from .. import utils

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

def get_user_by_user_id(db: Session, user_id: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user


async def user_create(user: User, user_data: utils.UserCreateModel, db: Session):
    user.name = user_data.name
    user.height = user_data.height
    user.weight = user_data.weight
    user.age = user_data.age
    user.gender = user_data.gender
    user.targetWeight = user_data.targetweight
    
    db.commit()
    db.refresh(user)

    return user

def users_read(db: Session):
    return db.query(User).all()

def user_read(db: Session, user_id: int):
    return db.query(User).filter(User.userId == user_id).first()

def delete_all_users(db: Session):
    db.query(User).delete()
    db.commit()