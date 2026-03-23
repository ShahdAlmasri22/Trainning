from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from .database import Base

class Role(Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    role = Column(SqlEnum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tasks = relationship("Task", back_populates="user", cascade="all, delete, save-update")
    logged = relationship("Logged", back_populates="user", cascade="all, delete, save-update")

