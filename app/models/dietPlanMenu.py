from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db.session import Base

# DietPlanMenu 모델 정의

class DietPlanMenu(Base):
    __tablename__ = 'DietPlanMenus'
    id = Column(Integer, primary_key=True, comment='Auto Increment')
    userDietId2 = Column(String(255), ForeignKey('UserDietPlans.id'), primary_key=True)
    menuId = Column(Integer, ForeignKey('Menus.id'), primary_key=True)
    id2 = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    meal_time = Column(String)