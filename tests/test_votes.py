import pytest

from app import models


@pytest.fixture
def test_vote(session, test_user, test_posts):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    response.status_code == 201


def test_vote_twice(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1}
    )
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 0}
    )
    assert response.status_code == 201


def test_delete_not_existing_vote(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "dir": 0}
    )
    assert response.status_code == 404


def test_vote_on_not_existing_post(authorized_client):
    response = authorized_client.post("/vote/", json={"post_id": 99999, "dir": 1})
    assert response.status_code == 404


def test_unauthorized_used_vote(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 401
