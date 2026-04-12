import enum
from sqlalchemy import Column,Integer,String ,DateTime,text,Float,Enum,ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint,CheckConstraint

class PaymentStatus(enum.Enum):
    pending = "PENDING"
    completed = "COMPLETED"
    failed = "FAILED"

class Payment(Base):
    __tablename__ = 'payments'

    __table_args__ = ()

    id = Column(Integer, primary_key = True , autoincrement = True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable = False)
    amount = Column(Float, nullable = False)
    payment_method = Column(String, nullable = False)
    payment_status = Column(Enum(PaymentStatus), nullable = False)
    transaction_id = Column(String, nullable = False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    ## relation ships
    order = relationship("orders",back_populates = "payments")



