from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db.session import Base

# DietPlanMenu 모델 정의
class DietPlanMenu(Base):
    __tablename__ = "DietPlanMenus"

    id = Column(String(255), ForeignKey("UserDietPlans.id"), primary_key=True)
    menuId = Column(Integer, ForeignKey("Menus.id"), primary_key=True)

    # UserDietPlan 모델과의 관계 정의
    user_diet_plan = relationship("UserDietPlan", back_populates="menu_items")
    # Menu 모델과의 관계 정의
    menu = relationship("Menu", back_populates="diet_plan_menus")