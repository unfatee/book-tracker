from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class QuoteCreate(BaseModel):
    text: str = Field(..., min_length=1)
    page: int | None = Field(None, gt=0)
    note: str | None = None


class QuoteUpdate(BaseModel):
    text: str | None = Field(None, min_length=1)
    page: int | None = Field(None, gt=0)
    note: str | None = None


class QuoteRead(BaseModel):
    id: int
    user_id: int
    book_id: int
    book_title: str | None = None
    text: str
    page: int | None
    note: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
