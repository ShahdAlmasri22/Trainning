from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    tasks = relationship("Task", back_populates="user", cascade="all, delete, save-update")

