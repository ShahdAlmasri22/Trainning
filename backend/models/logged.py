from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base



class Logged(Base):
    __tablename__='logged'
    logged_id = Column(Integer, autoincrement=True, primary_key=True)
    method = Column(String(10), nullable=False)
    path = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user=relationship("User", back_populates="logged")

