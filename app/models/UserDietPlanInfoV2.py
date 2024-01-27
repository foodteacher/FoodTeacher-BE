from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, TIMESTAMP, TEXT
from sqlalchemy.orm import relationship
from app.db.session import Base

class UserDietPlanInfoV2(Base):
    __tablename__ = 'UserDietPlanInfoV2'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='Auto Increment')
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True, comment='Auto Increment')
    created_at = Column(TIMESTAMP)
    advice = Column(TEXT)
    recommanded_exercise = Column(TEXT)
    menus = relationship("MenuV2")