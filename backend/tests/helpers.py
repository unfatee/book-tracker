def register_and_login(client, email="reader@example.com", password="secret123", name="Reader"):
    response = client.post(
        "/auth/register",
        json={"email": email, "password": password, "name": name},
    )
    assert response.status_code == 201
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_book(client, headers, **overrides):
    payload = {
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "Science Fiction",
        "total_pages": 688,
        "current_page": 0,
        "status": "want_to_read",
    }
    payload.update(overrides)
    response = client.post("/books", json=payload, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()
