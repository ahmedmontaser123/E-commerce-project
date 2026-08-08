import enum
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint


class ShippingAddress(Base):
    __tablename__  = 'shipping_addresses'
    __table_args__ = ()
    
    id = Column(Integer, primary_key = True , autoincrement = True)
    userid = Column(Integer, ForeignKey('users.id') , nullable = False)
    orderid = Column(Integer, ForeignKey('orders.id') , nullable = False)
    addressline1 = Column(String, nullable = False)
    addressline2 = Column(String, nullable = True)
    city = Column(String, nullable = False)
    postalcode = Column(String, nullable = False)
    country = Column(String, nullable = False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    ## relation ships
    user = relationship("User", back_populates="shipping_addresses")
    order = relationship("Order", back_populates="shipping_addresses")