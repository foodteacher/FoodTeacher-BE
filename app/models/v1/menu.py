from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base

class Menu(Base):
    __tablename__ = 'menu'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_id: Mapped[int] = mapped_column(ForeignKey('user_diet_plan_info.id'), comment='Auto Increment')
    name = Column(String(255))
    calories = Column(Float)
    meal_time = Column(String(255))
    created_at = Column(TIMESTAMP)
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="menus")