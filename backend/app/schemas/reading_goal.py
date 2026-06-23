from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReadingGoalCreate(BaseModel):
    year: int = Field(..., ge=1900, le=3000)
    target_books: int = Field(..., gt=0)


class ReadingGoalUpdate(BaseModel):
    target_books: int = Field(..., gt=0)


class ReadingGoalRead(BaseModel):
    id: int
    user_id: int
    year: int
    target_books: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReadingGoalProgress(BaseModel):
    year: int
    target_books: int
    completed_books: int
    progress_percent: float
    remaining_books: int
