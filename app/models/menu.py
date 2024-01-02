from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..db.session import Base

# Menu 모델 정의
class Menu(Base):
    __tablename__ = "Menus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    calories = Column(Float)

    # DietPlanMenu 모델과의 관계 정의
    diet_plan_menus = relationship("DietPlanMenu", back_populates="menu")