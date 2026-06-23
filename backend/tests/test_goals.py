from datetime import date

from tests.helpers import create_book, register_and_login


def test_goal_create_update_progress_and_delete(client):
    headers = register_and_login(client)
    year = date.today().year
    create_book(
        client,
        headers,
        title="Finished Book",
        total_pages=200,
        current_page=200,
        status="completed",
        finish_date=f"{year}-02-01",
    )

    created = client.post("/goals", json={"year": year, "target_books": 10}, headers=headers)
    assert created.status_code == 201
    assert created.json()["target_books"] == 10

    updated = client.put(f"/goals/{year}", json={"target_books": 5}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["target_books"] == 5

    progress = client.get(f"/goals/{year}/progress", headers=headers)
    assert progress.status_code == 200
    assert progress.json()["completed_books"] == 1
    assert progress.json()["progress_percent"] == 20

    deleted = client.delete(f"/goals/{year}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/goals/{year}", headers=headers).status_code == 404
