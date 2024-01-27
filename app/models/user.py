from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from ..db.session import Base

# User 모델 정의
class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, nullable=False, comment='Auto Increment')
    kakao_id = Column(String(255))
    name = Column(String(255))
    height = Column(Float)
    weight = Column(Float)
    age = Column(Integer)
    gender = Column(String(255))
    target_weight = Column(Float)
    kakao_access_token = Column(String(255))
    kakao_refresh_token = Column(String(255))
    jwt_refresh_token = Column(String(255))
    user_diet_plan_infos = relationship("UserDietPlanInfoV2")