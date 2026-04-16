import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth import get_current_user, create_access_token
from main import app


def test_view_user_200(client,admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id
    response = client.get("/users/view")

    assert response.status_code == 200
    assert "users" in response.json()


def test_view_user_403(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id
    response = client.get("/users/view")

    assert response.status_code == 403


def test_view_user_404(client):
    app.dependency_overrides[get_current_user] = lambda: 0
    response = client.get("/users/view")

    assert response.status_code == 404


def test_search_user_200(client, admin, db):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.get("/users/search?key=admin")

    assert response.json()["status_code"] == 200
    assert "users" in response.json()

def test_search_user_404(client):
    app.dependency_overrides[get_current_user] = lambda: 0

    response = client.get("/users/search?key=admin")

    assert response.status_code == 404


def test_search_user_403(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get("/users/search?key=admin")

    assert response.status_code == 403


def test_search_user_not_found(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.get("/users/search?key=no")

    assert response.json()["status_code"] == 404
    assert "users" not in response.json()


def test_create_user_200(client):
    response = client.post(
        "/users/",
        json={
            "name": "shahd",
            "email": "shahd@test.com",
            "password": "shahd1234*"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status_code"] == 201
    assert data["message"] == "✅ User created successfully"
    assert data["user"]["email"] == "shahd@test.com"
    assert "access_token" in data
    assert "refresh_token" in data


def test_create_user_422(client):
    response = client.post(
        "/users/",
        json={
            "name": "shahd",
            "email": "shahd@test.com",
            "password": "123"
        }
    )

    assert response.status_code == 422


def test_create_user_409(client, user):
    response = client.post(
        "/users/",
        json={
            "name": "shahd",
            "email": "user@test.com",
            "password": "shahd1234*"
        }
    )

    assert response.status_code == 409
    assert "already in use" in response.json()["detail"]


def test_login_200(client, user):
    response = client.post(
        "/users/login",
        json={
            "email": "user@test.com",
            "password": "user1234*"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "✅ Login successfully"
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user_id"] is not None


def test_login_user_404(client):
    response = client.post(
        "/users/login",
        json={
            "email": "notfound@test.com",
            "password": "12345678"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_login_401(client, user):
    response = client.post(
        "/users/login",
        json={
            "email": "user@test.com",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong password!"


def test_update_profile_200(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.patch(
        f"/users/profile/{user.user_id}",
        json={
            "name": "new_name"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User info updated successfully"


def test_update_profile_404(client, user):
    app.dependency_overrides[get_current_user] = lambda: 0

    response = client.patch(
        f"/users/profile/{0}",
        json={
            "name": "new_name"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_profile_403(client, user, admin):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.patch(
        f"/users/profile/{admin.user_id}",
        json={
            "name": "new_name"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission"



def test_update_password_200(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.patch(
        f"/users/profile/{admin.user_id}",
        json={
            "old_password": "admin1234*",
            "new_password": "newpass123*"
        }
    )

    assert response.status_code == 200


def test_update_password_403(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.patch(
        f"/users/profile/{admin.user_id}",
        json={
            "old_password": "admin12",
            "new_password": "newpass123*"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Wrong password"


def test_update_password_404(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.patch(
        f"/users/profile/{admin.user_id}",
        json={
            "new_password": "newpass123*"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Old password required"



def test_delete_user_200(client, admin, user):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.delete(f"/users/{user.user_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"


def test_delete_user_404(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.delete("/users/0")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_403(client, user, admin):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.delete(f"/users/{admin.user_id}")

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to delete account"


def test_update_role_200(client, user, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.patch(f"/users/role/{user.user_id}",
            params={
            "new_role": "ADMIN"
        })

    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"


def test_update_role_user_updated_not_found(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.patch("/users/role/0",
            params={
            "new_role": "ADMIN"
        })

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_role_admin_do_the_req_not_found(client, user):
    app.dependency_overrides[get_current_user] = lambda: 0

    response = client.patch(f"/users/role/{user.user_id }",
            params={
            "new_role": "ADMIN"
        })

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_role_403(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.patch(f"/users/role/{user.user_id}",
            params={
            "new_role": "ADMIN"
        })

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to change role"


def test_refresh(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.post("/users/refresh")

    assert response.status_code == 200
    assert "access_token" in response.json()
