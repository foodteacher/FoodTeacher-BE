from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..db.session import Base

# UserDietPlan 모델 정의
class UserDietPlan(Base):
    __tablename__ = "UserDietPlans"

    id = Column(String(255), primary_key=True)
    userId = Column(Integer, ForeignKey("Users.userId"), nullable=False)
    description = Column(Text)

    # User 모델과의 관계 정의
    user = relationship("User", back_populates="diet_plans")
    # DietPlanMenu 모델과의 관계 정의
    menu_items = relationship("DietPlanMenu", back_populates="user_diet_plan")