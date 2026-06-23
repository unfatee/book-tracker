from tests.helpers import register_and_login


def test_register_duplicate_login_and_me(client):
    headers = register_and_login(client)

    duplicate = client.post(
        "/auth/register",
        json={"email": "reader@example.com", "password": "secret123", "name": "Reader"},
    )
    assert duplicate.status_code == 409

    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "reader@example.com"
    assert "hashed_password" not in me.json()


def test_login_rejects_wrong_password(client):
    register_and_login(client)
    response = client.post("/auth/login", json={"email": "reader@example.com", "password": "bad"})
    assert response.status_code == 401
