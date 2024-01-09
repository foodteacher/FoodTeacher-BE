from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class UserDietPlanInfo(Base):
    __tablename__ = 'UserDietPlanInfo'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Auto Increment')
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True, comment='Auto Increment')
    menus = relationship("Menu")