from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db.session import Base

# DietPlanMenu 모델 정의

class DietPlanMenu(Base):
    __tablename__ = 'DietPlanMenus'
    id = Column(Integer, primary_key=True, nullable=False, comment='Auto Increment')
    userDietId2 = Column(String(255), ForeignKey('UserDietPlans.id'), primary_key=True, comment='Auto Increment')
    menuId = Column(Integer, ForeignKey('Menus.id'), primary_key=True, comment='Auto Increment')
    userDietPlan = relationship("UserDietPlan")
    menu = relationship("Menu")