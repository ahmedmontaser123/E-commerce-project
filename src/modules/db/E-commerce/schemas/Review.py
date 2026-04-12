import enum
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint

class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
         CheckConstraint('rating >= 1 AND rating <= 5', name='check_review_rating_range'),
    )
    
    id = Column(Integer, primary_key = True , autoincrement = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable = False)
    rating = Column(Integer, nullable = False)
    comment = Column(String, nullable = True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ## relation ships
    users = relationship("users", back_populates="reviews")
    products = relationship("products", back_populates="reviews")
