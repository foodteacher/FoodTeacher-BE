from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..db.session import Base

# UserDietPlan 모델 정의

class UserDietPlan(Base):
    __tablename__ = 'UserDietPlans'
    id = Column(String(255), primary_key=True, nullable=False, comment='Auto Increment')
    description = Column(Text)