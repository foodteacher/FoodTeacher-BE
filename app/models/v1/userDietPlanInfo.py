from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship, Mapped
from app.db.session import Base
from app.models.v1.menu import Menu
from app.models.v1.exercise import Exercise
from typing import List

class UserDietPlanInfo(Base):
    __tablename__ = 'user_diet_plan_info'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Auto Increment')
    user_id = Column(Integer, ForeignKey('user.id'), comment='Auto Increment')
    user: Mapped["User"] = relationship(back_populates="user_diet_plan_info")
    menus: Mapped[List["Menu"]] = relationship(back_populates="user_diet_plan_info")
    exercise: Mapped["Exercise"] = relationship(back_populates="user_diet_plan_info")