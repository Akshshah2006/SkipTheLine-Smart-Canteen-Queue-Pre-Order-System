from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    course = Column(String, default="B.Tech")
    year = Column(Integer, default=3)
    verified = Column(Boolean, default=False)
    login_time = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    items = Column(Text)                    # stored as JSON string
    pickup_time = Column(String)
    status = Column(String, default="waiting")
    token = Column(Integer, unique=True, nullable=False)
    barcode_path = Column(String, nullable=True)
    payment_status = Column(String, default="pending")
    total_amount = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
