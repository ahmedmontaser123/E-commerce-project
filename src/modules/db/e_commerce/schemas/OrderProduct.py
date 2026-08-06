import enum
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint


class OrderProduct(Base):
    __tablename__ = 'orderproducts'

    __table_args__ = ()
    
    id = Column(Integer, primary_key = True , autoincrement = True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable = False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable = False)
    quantity = Column(Integer, nullable = False)


    ## relation ships
    order = relationship("Order", back_populates="order_products")
    products = relationship("Product", back_populates="order_products")
