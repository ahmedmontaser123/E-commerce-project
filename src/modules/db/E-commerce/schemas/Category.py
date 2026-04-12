# import libraries
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint


class Category(Base):
    __tablename__ = 'categories'


    __table_args__ = (
       UniqueConstraint('name', name='uq_category_name'),
   )
    
    id = Column(Integer, primary_key = True , autoincrement = True)
    name = Column(String, nullable = False)

    # relation ship
    Products = relationship("products", back_populates="categories")


