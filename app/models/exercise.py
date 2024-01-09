from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Exercise(Base):
    __tablename__ = 'Exercise'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_id = Column(Integer, ForeignKey('UserDietPlanInfo.id'), primary_key=True, comment='Auto Increment')
    advice = Column(Text)
    recommended_exercise = Column(Text)