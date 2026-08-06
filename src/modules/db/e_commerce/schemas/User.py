# import libraries
import enum

from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,Boolean
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint


class UserRole(enum.Enum):
      User = "user"
      Admin = "admin"


class User(Base):

    __tablename__ = 'users'


        
    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
        UniqueConstraint('password', name='uq_user_password'),
    )


    id = Column(Integer, primary_key = True, autoincrement = True)
    email = Column(String,nullable = False )
    role = Column(Enum(UserRole), default=UserRole.User, nullable=False)
    password = Column(String,nullable = False)
    name = Column(String,nullable = False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
       
    # relationships
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    cart = relationship("Cart", back_populates="user", cascade = "all, delete-orphan")
    wishlist = relationship("Wishlist", back_populates="user",cascade = "all, delete-orphan")
    shipping_addresses = relationship("ShippingAddress", back_populates="user")

