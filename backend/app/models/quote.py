from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils.dates import utc_now


class Quote(Base):
    __tablename__ = "quotes"
    __table_args__ = (
        CheckConstraint("page IS NULL OR page > 0", name="ck_quotes_page_positive"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    page = Column(Integer, nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    owner = relationship("User", back_populates="quotes")
    book = relationship("Book", back_populates="quotes")

    @property
    def book_title(self) -> str | None:
        return self.book.title if self.book else None
