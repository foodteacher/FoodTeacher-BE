from .base_class import Base
from .models.dietPlanMenu import DietPlanMenu
from .models.menu import Menu
from .models.user import User
from .models.userDietPlan import UserDietPlan

from sqlalchemy.orm import Session

from ..utils import UserBaseModel

def user_create(db: Session, user_data: UserBaseModel):
    # User 모델을 사용하여 새로운 사용자 데이터 생성
    new_user = User(
    name=user_data.name,
    height=user_data.height,
    weight=user_data.weight,
    age=user_data.age,
    gender=user_data.gender,
    targetWeight=user_data.targetWeight,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def users_read(db: Session):
    return db.query(User).all()

def user_read(db: Session, user_id: int):
    return db.query(User).filter(User.userId == user_id).first()

def delete_all_users(db: Session):
    db.query(User).delete()
    db.commit()