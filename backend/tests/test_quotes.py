from tests.helpers import create_book, register_and_login


def test_quote_crud_and_search(client):
    headers = register_and_login(client)
    book = create_book(client, headers, total_pages=300)

    created = client.post(
        f"/books/{book['id']}/quotes",
        json={"text": "A memorable line.", "page": 12, "note": "Important"},
        headers=headers,
    )
    assert created.status_code == 201
    quote_id = created.json()["id"]

    book_quotes = client.get(f"/books/{book['id']}/quotes", headers=headers)
    assert book_quotes.status_code == 200
    assert len(book_quotes.json()) == 1

    all_quotes = client.get("/quotes?search=memorable", headers=headers)
    assert all_quotes.status_code == 200
    assert all_quotes.json()[0]["book_title"] == "Dune"

    updated = client.put(
        f"/books/{book['id']}/quotes/{quote_id}",
        json={"text": "An updated line.", "page": 20},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["page"] == 20

    deleted = client.delete(f"/books/{book['id']}/quotes/{quote_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/books/{book['id']}/quotes", headers=headers).json() == []


def test_user_cannot_access_another_users_quote(client):
    owner_headers = register_and_login(client, email="owner@example.com")
    stranger_headers = register_and_login(client, email="stranger@example.com")
    book = create_book(client, owner_headers)
    quote = client.post(
        f"/books/{book['id']}/quotes",
        json={"text": "Private highlight"},
        headers=owner_headers,
    ).json()

    response = client.put(
        f"/books/{book['id']}/quotes/{quote['id']}",
        json={"text": "No access"},
        headers=stranger_headers,
    )
    assert response.status_code == 404


def test_quote_page_cannot_exceed_book_pages(client):
    headers = register_and_login(client)
    book = create_book(client, headers, total_pages=50)
    response = client.post(
        f"/books/{book['id']}/quotes",
        json={"text": "Impossible page", "page": 51},
        headers=headers,
    )
    assert response.status_code == 400
