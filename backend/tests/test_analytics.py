from datetime import date

from tests.helpers import create_book, register_and_login


def test_summary_by_genre_and_monthly_reading(client):
    headers = register_and_login(client)
    year = date.today().year
    client.post("/goals", json={"year": year, "target_books": 4}, headers=headers)
    create_book(
        client,
        headers,
        title="Dune",
        genre="Science Fiction",
        total_pages=688,
        current_page=688,
        status="completed",
        rating=5,
        finish_date=f"{year}-03-10",
    )
    create_book(
        client,
        headers,
        title="Clean Code",
        author="Robert C. Martin",
        genre="Programming",
        total_pages=464,
        current_page=100,
        status="reading",
        rating=5,
    )

    summary = client.get("/analytics/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_books"] == 2
    assert summary.json()["completed_books"] == 1
    assert summary.json()["current_year_goal_progress"] == 25

    by_genre = client.get("/analytics/by-genre", headers=headers)
    assert by_genre.status_code == 200
    assert {item["genre"] for item in by_genre.json()} == {"Science Fiction", "Programming"}

    monthly = client.get(f"/analytics/monthly-reading?year={year}", headers=headers)
    assert monthly.status_code == 200
    assert monthly.json()[2]["month"] == "March"
    assert monthly.json()[2]["completed_books"] == 1

    top_authors = client.get("/analytics/top-authors", headers=headers)
    assert top_authors.status_code == 200
    assert len(top_authors.json()) == 2
