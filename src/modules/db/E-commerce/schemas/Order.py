import enum
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint

class orderstatus(enum.Enum):
    pending = "PENDING"
    completed = "COMPLETED"
    cancelled = "CANCELLED"


class Order(Base):
    __tablename__ = 'orders'

    __table_args__ = ()

    id = Column(Integer, primary_key = True , autoincrement = True)
    userid = Column(Integer, ForeignKey('users.id') , nullable = False)
    total = Column(Float , nullable = False)
    status = Column(Enum(orderstatus), default=orderstatus.pending, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    ## relation ships
    orderproducts = relationship("orderproducts", back_populates="orders")
    users = relationship("users", back_populates = "orders")

