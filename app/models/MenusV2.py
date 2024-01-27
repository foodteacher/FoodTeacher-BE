from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.session import Base

class MenusV2(Base):
    __tablename__ = 'MenusV2'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_id = Column(Integer, ForeignKey('UserDietPlanInfoV2.id'), primary_key=True, comment='Auto Increment')
    name = Column(String(255))
    calories = Column(Float)
    car = Column(Float)
    pro = Column(Float)
    fat = Column(Float)
    meal_time = Column(String(255))