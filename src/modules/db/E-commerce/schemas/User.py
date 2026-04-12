# import libraries
import enum

from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint


class userRole(enum.Enum):
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
    role = Column(Enum(userRole), default=userRole.User, nullable=False)
    password = Column(String,nullable = False)
    name = Column(String,nullable = False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
       
    # relationships
    orders = relationship("orders", back_populates="users")
    reviews = relationship("reviews", back_populates="users")
    cart = relationship("carts", back_populates="users", uselist=False)
    wishlist = relationship("wishlists", back_populates="users", uselist=False)
    shipping_addresses = relationship("shipping_addresses", back_populates="users")

