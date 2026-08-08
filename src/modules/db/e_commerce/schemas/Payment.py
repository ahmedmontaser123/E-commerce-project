import enum
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint

class PaymentStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"


class PaymentMethod(enum.Enum):
    CARD = "card"
    CASH = "cash"
    WALLET = "wallet"

class Payment(Base):
    __tablename__ = 'payments'

    __table_args__ = ()

    id = Column(Integer, primary_key = True , autoincrement = True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable = False)
    amount = Column(Float, nullable = False)
    payment_method = Column(Enum(PaymentMethod),default=PaymentMethod.CARD, nullable = False)
    payment_status = Column(Enum(PaymentStatus),default=PaymentStatus.PENDING, nullable = False)
    transaction_id = Column(String, nullable = False,unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    ## relation ships
    order = relationship("Order", back_populates="payments")



