from tests.helpers import create_book, register_and_login


def test_book_crud_progress_favorite_status_and_csv(client):
    headers = register_and_login(client)
    book = create_book(client, headers, title="Clean Code", author="Robert C. Martin", total_pages=464)

    listing = client.get("/books?search=clean&sort_by=title&sort_order=asc", headers=headers)
    assert listing.status_code == 200
    assert len(listing.json()) == 1

    detail = client.get(f"/books/{book['id']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["title"] == "Clean Code"

    updated = client.put(
        f"/books/{book['id']}",
        json={"genre": "Programming", "rating": 5, "current_page": 120},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["rating"] == 5

    progress = client.patch(f"/books/{book['id']}/progress", json={"current_page": 464}, headers=headers)
    assert progress.status_code == 200
    assert progress.json()["status"] == "completed"
    assert progress.json()["progress_percent"] == 100

    favorite = client.patch(f"/books/{book['id']}/favorite", headers=headers)
    assert favorite.status_code == 200
    assert favorite.json()["is_favorite"] is True

    status_response = client.patch(f"/books/{book['id']}/status", json={"status": "reading"}, headers=headers)
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "reading"
    assert status_response.json()["finish_date"] is None

    csv_response = client.get("/books/export/csv", headers=headers)
    assert csv_response.status_code == 200
    assert "Clean Code" in csv_response.text

    deleted = client.delete(f"/books/{book['id']}", headers=headers)
    assert deleted.status_code == 204
    missing = client.get(f"/books/{book['id']}", headers=headers)
    assert missing.status_code == 404


def test_user_cannot_get_another_users_book(client):
    owner_headers = register_and_login(client, email="owner@example.com")
    stranger_headers = register_and_login(client, email="stranger@example.com", name="Stranger")
    book = create_book(client, owner_headers)

    response = client.get(f"/books/{book['id']}", headers=stranger_headers)
    assert response.status_code == 404


def test_current_page_cannot_exceed_total_pages(client):
    headers = register_and_login(client)
    response = client.post(
        "/books",
        json={"title": "Too Far", "author": "Tester", "total_pages": 100, "current_page": 101},
        headers=headers,
    )
    assert response.status_code == 400
