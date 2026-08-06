from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint


class Product(Base):
    __tablename__  = 'products'

    __table_args__ = (
         UniqueConstraint('name', name='uq_product_name'),
         CheckConstraint('price >= 0', name='check_product_price_non_negative'),
         CheckConstraint('stock >= 0', name='check_product_stock_non_negative')
        
    )


    id = Column(Integer, primary_key = True , autoincrement = True)
    name = Column(String, nullable = False)
    description = Column(String, nullable = False)
    price = Column(Float, nullable = False)
    stock = Column(Integer, nullable = False, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relation ships 
    categories = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates = "products",cascade = "all, delete-orphan")
    wishlist = relationship("Wishlist", back_populates = "products")
    order_products = relationship("OrderProduct", back_populates="products")
    cart_products = relationship(
    "CartProduct",
    back_populates="product"
    )     
    
    



