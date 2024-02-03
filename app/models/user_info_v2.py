from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from datetime import datetime

from app.db.session import Base

class UserV2(Base):
    __tablename__ = 'user_v2'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    kakao_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    height: Mapped[float] = mapped_column(nullable=True)
    weight: Mapped[float] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(255), nullable=True)
    target_weight: Mapped[float] = mapped_column(nullable=True)
    kakao_access_token: Mapped[str] = mapped_column(String(255))
    kakao_refresh_token: Mapped[str] = mapped_column(String(255))
    jwt_refresh_token: Mapped[str] = mapped_column(String(255))
    user_diet_plan_info_v2: Mapped["UserDietPlanInfoV2"] = relationship(back_populates="user")


class UserDietPlanInfoV2(Base):
    __tablename__ = 'user_diet_plan_info_v2'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_v2_id: Mapped[int] = mapped_column(ForeignKey('user_v2.id'), comment='Auto Increment')
    created_at: Mapped[datetime] = mapped_column(nullable=True)
    advice: Mapped[str] = mapped_column(nullable=True)
    recommanded_exercise: Mapped[str] = mapped_column(nullable=True)
    excess_calories: Mapped[float] = mapped_column(nullable=True)
    user: Mapped["UserV2"] = relationship(back_populates="user_diet_plan_info_v2")
    menus: Mapped[List["MenuV2"]] = relationship(back_populates="user_diet_plan_info_v2")
    exercise: Mapped[List["ExerciseV2"]] = relationship(back_populates="user_diet_plan_info_v2")


class MenuV2(Base):
    __tablename__ = 'menu_v2'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_v2_id: Mapped[int] = mapped_column(ForeignKey('user_diet_plan_info_v2.id'), comment='Auto Increment')
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    calories: Mapped[float] = mapped_column(nullable=True)
    car: Mapped[float] = mapped_column(nullable=True)
    pro: Mapped[float] = mapped_column(nullable=True)
    fat: Mapped[float] = mapped_column(nullable=True)
    meal_time: Mapped[str] = mapped_column(String(255), nullable=True)
    user_diet_plan_info_v2: Mapped["UserDietPlanInfoV2"] = relationship(back_populates="menus")


class ExerciseV2(Base):
    __tablename__ = 'exercise_v2'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_v2_id: Mapped[int] = mapped_column(ForeignKey('user_diet_plan_info_v2.id'), comment='Auto Increment')
    my_exercise: Mapped[str] = mapped_column(nullable=True)
    my_exercise_calories: Mapped[float] = mapped_column(nullable=True)
    user_diet_plan_info_v2: Mapped["UserDietPlanInfoV2"] = relationship(back_populates="exercise_v2")