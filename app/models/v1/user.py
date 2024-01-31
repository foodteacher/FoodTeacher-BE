from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.models.v1.userDietPlanInfo import UserDietPlanInfo

from app.db.session import Base

# User 모델 정의
class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    kakao_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    height: Mapped[float] = mapped_column(nullable=True)
    weight: Mapped[float] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(255), nullable=True)
    target_weight: Mapped[float] = mapped_column(nullable=True)
    kakao_access_token: Mapped[str] = mapped_column(String(255))
    kakao_refresh_token: Mapped[str] = mapped_column(String(255))
    jwt_refresh_token: Mapped[str] = mapped_column(String(255))
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="user")