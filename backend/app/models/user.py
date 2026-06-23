from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.dates import utc_now


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    books = relationship("Book", back_populates="owner", cascade="all, delete-orphan")
    quotes = relationship("Quote", back_populates="owner", cascade="all, delete-orphan")
    goals = relationship("ReadingGoal", back_populates="owner", cascade="all, delete-orphan")
