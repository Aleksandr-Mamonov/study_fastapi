import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return schemas.Post(**post)

    posts_map = map(validate, response.json())
    # print(list(posts_map))
    posts_list = list(posts_map)

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200
    assert posts_list[0].id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_not_existing_post(authorized_client):
    response = authorized_client.get(f"/posts/999999")
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(response.json())
    post = schemas.Post(**response.json())
    # print()
    # print(post)
    # print()
    # print(test_posts)
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("new title", "new content", True),
        ("newly created post", "some content", False),
        ("new post about ..", "still in work", False),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]
    assert created_post.owner.email == test_user["email"]


def test_create_post_default_published_true(authorized_client):
    response = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"}
    )
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True


def test_unauthorized_user_create_post(client):
    response = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "arbitrary content"}
    )
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(
        f"/posts/{test_posts[0].id}",
    )
    assert response.status_code == 401


def test_delete_post_successfully(authorized_client, test_posts):
    response = authorized_client.delete(
        f"/posts/{test_posts[0].id}",
    )
    assert response.status_code == 204


def test_delete_not_existing_post(authorized_client):
    response = authorized_client.delete("/posts/999999")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    response = client.put(
        f"/posts/{test_posts[0].id}",
    )
    assert response.status_code == 401


def test_update_not_existing_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    response = authorized_client.put("/posts/999999", json=data)

    assert response.status_code == 404
