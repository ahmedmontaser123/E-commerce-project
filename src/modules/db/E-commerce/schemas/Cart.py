import enum
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key = True , autoincrement = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    ## relation ships
    users = relationship("users", back_populates="carts" , uselist = False)
    cartproducts = relationship("cartproducts", back_populates="carts")

