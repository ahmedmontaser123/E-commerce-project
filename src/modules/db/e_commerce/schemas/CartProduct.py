import enum
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint

class CartProduct(Base):
    __tablename__ = 'cart_products'
    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),
        CheckConstraint('quantity > 0', name='check_cart_product_quantity_positive')
    )

    id = Column(Integer, primary_key = True , autoincrement = True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable = False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable = False)
    quantity = Column(Integer, nullable = False)



    cart = relationship(
        "Cart",
        back_populates="cart_products"
    )

    product = relationship(
        "Product",
        back_populates="cart_products"
    )
  
