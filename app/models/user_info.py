from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from app.db.session import Base

class User(Base):
    __tablename__ = 'user'
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
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="user")


class UserDietPlanInfo(Base):
    __tablename__ = 'user_diet_plan_info'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), comment='Auto Increment')
    user: Mapped["User"] = relationship(back_populates="user_diet_plan_info")
    menus: Mapped[List["Menu"]] = relationship(back_populates="user_diet_plan_info")
    exercise: Mapped["Exercise"] = relationship(back_populates="user_diet_plan_info")


class Menu(Base):
    __tablename__ = 'menu'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_id: Mapped[int] = mapped_column(ForeignKey('user_diet_plan_info.id'), comment='Auto Increment')
    name = Column(String(255))
    calories = Column(Float)
    meal_time = Column(String(255))
    created_at = Column(TIMESTAMP)
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="menus")


class Exercise(Base):
    __tablename__ = 'exercise'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_id = Column(Integer, ForeignKey('user_diet_plan_info.id'), comment='Auto Increment')
    advice = Column(Text)
    recommended_exercise = Column(Text)
    excess_calories = Column(Float)
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="exercise")