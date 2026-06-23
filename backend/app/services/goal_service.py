from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.reading_goal import ReadingGoal
from app.models.user import User
from app.schemas.reading_goal import ReadingGoalCreate, ReadingGoalProgress, ReadingGoalUpdate


def list_goals(db: Session, user: User) -> list[ReadingGoal]:
    return db.query(ReadingGoal).filter(ReadingGoal.user_id == user.id).order_by(ReadingGoal.year.desc()).all()


def get_goal_or_404(db: Session, user: User, year: int) -> ReadingGoal:
    goal = db.query(ReadingGoal).filter(ReadingGoal.user_id == user.id, ReadingGoal.year == year).first()
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading goal not found")
    return goal


def create_or_update_goal(db: Session, user: User, payload: ReadingGoalCreate) -> ReadingGoal:
    goal = db.query(ReadingGoal).filter(ReadingGoal.user_id == user.id, ReadingGoal.year == payload.year).first()
    if goal:
        goal.target_books = payload.target_books
    else:
        goal = ReadingGoal(user_id=user.id, year=payload.year, target_books=payload.target_books)
        db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def update_goal(db: Session, user: User, year: int, payload: ReadingGoalUpdate) -> ReadingGoal:
    goal = get_goal_or_404(db, user, year)
    goal.target_books = payload.target_books
    db.commit()
    db.refresh(goal)
    return goal


def delete_goal(db: Session, user: User, year: int) -> None:
    goal = get_goal_or_404(db, user, year)
    db.delete(goal)
    db.commit()


def get_goal_progress(db: Session, user: User, year: int) -> ReadingGoalProgress:
    goal = get_goal_or_404(db, user, year)
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    completed = (
        db.query(Book)
        .filter(
            Book.user_id == user.id,
            Book.status == "completed",
            Book.finish_date >= start,
            Book.finish_date <= end,
        )
        .count()
    )
    progress = round((completed / goal.target_books) * 100, 2)
    return ReadingGoalProgress(
        year=year,
        target_books=goal.target_books,
        completed_books=completed,
        progress_percent=progress,
        remaining_books=max(goal.target_books - completed, 0),
    )
