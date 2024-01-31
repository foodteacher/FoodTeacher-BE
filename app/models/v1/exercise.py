from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship, Mapped
from app.db.session import Base
from typing import Optional

class Exercise(Base):
    __tablename__ = 'exercise'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_id = Column(Integer, ForeignKey('user_diet_plan_info.id'), comment='Auto Increment')
    advice = Column(Text)
    recommended_exercise = Column(Text)
    excess_calories = Column(Float)
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="exercise")