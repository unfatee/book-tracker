"""Initial database schema.

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)

    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("genre", sa.String(length=120), nullable=True),
        sa.Column("total_pages", sa.Integer(), nullable=False),
        sa.Column("current_page", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("cover_url", sa.String(length=500), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("finish_date", sa.Date(), nullable=True),
        sa.Column("is_favorite", sa.Boolean(), nullable=False),
        sa.Column("personal_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("current_page >= 0", name="ck_books_current_page_non_negative"),
        sa.CheckConstraint("current_page <= total_pages", name="ck_books_current_page_lte_total"),
        sa.CheckConstraint("rating IS NULL OR (rating >= 1 AND rating <= 5)", name="ck_books_rating_range"),
        sa.CheckConstraint("total_pages > 0", name="ck_books_total_pages_positive"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_books_author", "books", ["author"], unique=False)
    op.create_index("ix_books_finish_date", "books", ["finish_date"], unique=False)
    op.create_index("ix_books_genre", "books", ["genre"], unique=False)
    op.create_index("ix_books_id", "books", ["id"], unique=False)
    op.create_index("ix_books_is_favorite", "books", ["is_favorite"], unique=False)
    op.create_index("ix_books_rating", "books", ["rating"], unique=False)
    op.create_index("ix_books_status", "books", ["status"], unique=False)
    op.create_index("ix_books_title", "books", ["title"], unique=False)
    op.create_index("ix_books_user_id", "books", ["user_id"], unique=False)

    op.create_table(
        "reading_goals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("target_books", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("target_books > 0", name="ck_reading_goals_target_positive"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "year", name="uq_reading_goals_user_year"),
    )
    op.create_index("ix_reading_goals_id", "reading_goals", ["id"], unique=False)
    op.create_index("ix_reading_goals_user_id", "reading_goals", ["user_id"], unique=False)
    op.create_index("ix_reading_goals_year", "reading_goals", ["year"], unique=False)

    op.create_table(
        "quotes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("page IS NULL OR page > 0", name="ck_quotes_page_positive"),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_quotes_book_id", "quotes", ["book_id"], unique=False)
    op.create_index("ix_quotes_id", "quotes", ["id"], unique=False)
    op.create_index("ix_quotes_user_id", "quotes", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_quotes_user_id", table_name="quotes")
    op.drop_index("ix_quotes_id", table_name="quotes")
    op.drop_index("ix_quotes_book_id", table_name="quotes")
    op.drop_table("quotes")
    op.drop_index("ix_reading_goals_year", table_name="reading_goals")
    op.drop_index("ix_reading_goals_user_id", table_name="reading_goals")
    op.drop_index("ix_reading_goals_id", table_name="reading_goals")
    op.drop_table("reading_goals")
    op.drop_index("ix_books_user_id", table_name="books")
    op.drop_index("ix_books_title", table_name="books")
    op.drop_index("ix_books_status", table_name="books")
    op.drop_index("ix_books_rating", table_name="books")
    op.drop_index("ix_books_is_favorite", table_name="books")
    op.drop_index("ix_books_id", table_name="books")
    op.drop_index("ix_books_genre", table_name="books")
    op.drop_index("ix_books_finish_date", table_name="books")
    op.drop_index("ix_books_author", table_name="books")
    op.drop_table("books")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
