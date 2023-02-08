import pytest
from app import schemas
from jose import jwt

from app.config import settings


# def test_root(client):
#     response = client.get("/")
#     # print(response.json().get("message"))
#     assert response.json().get("message") == "Hello World"
#     assert response.status_code == 200


def test_create_user(client):
    # using trailing slash in path, e.g. '/users/' instead of '/users' because latter would redirect to former
    # and status code would be 307 Redirect, and only then - 201 Created.
    response = client.post(
        "/users/", json={"email": "example@example.com", "password": "examplepassword"}
    )
    # print(response.json())
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "example@example.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrong_email@mail.com", "example_password", 403),
        ("example@example.com", "wrong_password", 403),
        ("wrong_email@example.com", "wrong_password_as_well", 403),
        (None, "password", 422),
        ("example@example.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
