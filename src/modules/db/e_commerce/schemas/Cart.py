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
    user = relationship("User", back_populates="cart")
    cart_products = relationship("CartProduct", back_populates="cart",cascade = "all, delete-orphan")

