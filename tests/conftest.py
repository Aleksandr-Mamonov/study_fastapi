"""Each fixture defined in this file will be automatically accessable by all tests in this 'tests' package
In each test module there's no need to import conftest. It would be automatically imported by pytest.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token


# Creating test_database

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip_address(or hostname)>:<port>/<database_name>"
# For testing purposes we can just hardcode database_url. Or just change db_name by adding '_test'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Command to test test_users.py: pytest -v -s -x --disable-warnings tests/test_users.py
# -x flag = pytest stops after the first failed test


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "example@example.com", "password": "example_password"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_2(client):
    user_data = {"email": "example2@example.com", "password": "example2_password"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user_2, session):
    posts_data = [
        {
            "title": "first post TITLE!",
            "content": "some content here",
            "owner_id": test_user["id"],
        },
        {
            "title": "second post TITLE!",
            "content": "another line of content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third post TITLE!",
            "content": "more content coming in",
            "owner_id": test_user["id"],
        },
        {
            "title": "another user post TITLE!",
            "content": "more content coming in",
            "owner_id": test_user_2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)

    session.add_all(list(post_map))
    session.commit()
    posts = session.query(models.Post).all()
    return posts
