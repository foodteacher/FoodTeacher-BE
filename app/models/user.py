from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from ..db.session import Base

# User 모델 정의
class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kakao_id = Column(String(255))
    name = Column(String(255))
    height = Column(Float)
    weight = Column(Float)
    age = Column(Integer)
    gender = Column(String(255))
    targetWeight = Column(Float)

    # UserDietPlan과의 관계 정의
    diet_plans = relationship("UserDietPlan", back_populates="user")