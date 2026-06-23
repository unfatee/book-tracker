from sqlalchemy import Boolean, CheckConstraint, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.dates import utc_now


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint("total_pages > 0", name="ck_books_total_pages_positive"),
        CheckConstraint("current_page >= 0", name="ck_books_current_page_non_negative"),
        CheckConstraint("current_page <= total_pages", name="ck_books_current_page_lte_total"),
        CheckConstraint("rating IS NULL OR (rating >= 1 AND rating <= 5)", name="ck_books_rating_range"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    genre = Column(String(120), nullable=True, index=True)
    total_pages = Column(Integer, nullable=False)
    current_page = Column(Integer, default=0, nullable=False)
    status = Column(String(32), default="want_to_read", nullable=False, index=True)
    rating = Column(Integer, nullable=True, index=True)
    cover_url = Column(String(500), nullable=True)
    start_date = Column(Date, nullable=True)
    finish_date = Column(Date, nullable=True, index=True)
    is_favorite = Column(Boolean, default=False, nullable=False, index=True)
    personal_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    owner = relationship("User", back_populates="books")
    quotes = relationship("Quote", back_populates="book", cascade="all, delete-orphan")

    @property
    def progress_percent(self) -> float:
        if not self.total_pages:
            return 0.0
        return round((self.current_page / self.total_pages) * 100, 2)
