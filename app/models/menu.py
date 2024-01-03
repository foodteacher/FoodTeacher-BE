from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..db.session import Base

# Menu 모델 정의
class Menu(Base):
    __tablename__ = 'Menus'
    id = Column(Integer, primary_key=True, nullable=False, comment='Auto Increment')
    name = Column(String)
    calories = Column(Float)