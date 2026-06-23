from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.dates import utc_now


class ReadingGoal(Base):
    __tablename__ = "reading_goals"
    __table_args__ = (
        UniqueConstraint("user_id", "year", name="uq_reading_goals_user_year"),
        CheckConstraint("target_books > 0", name="ck_reading_goals_target_positive"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    target_books = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    owner = relationship("User", back_populates="goals")
