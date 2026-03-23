from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, ForeignKey, DateTime
from enum import Enum
from sqlalchemy.orm import relationship
from .database import Base


class Status(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'

class Priority(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

class Task(Base):
    __tablename__='tasks'
    task_id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(25), nullable=False)
    description = Column(String(50), nullable=False)
    status = Column(SqlEnum(Status), nullable=False)
    priority = Column(SqlEnum(Priority), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    user=relationship("User", back_populates="tasks")
