import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.auth import get_current_user
from main import app


def test_create_task_200(client,admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id
    response = client.post("/tasks/",
               json={
                   "title": "test ",
                   "description": "test task",
                   "priority": "LOW"
               }
               )

    assert response.status_code == 200
    assert response.json()["message"] == "✅ Task created successfully"
    assert "task" in response.json()


def test_create_task_404(client):
    app.dependency_overrides[get_current_user] = lambda: 0
    response = client.post("/tasks/",
               json={
                   "title": "test ",
                   "description": "test task",
                   "priority": "LOW"
               }
               )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_view_task_200(client, user, task):
    app.dependency_overrides[get_current_user] = lambda: user.user_id
    response = client.get("/tasks/view")

    assert response.status_code == 200
    assert "total_tasks" in response.json()
    assert "tasks" in response.json()


def test_view_status_200(client, user, task):
    app.dependency_overrides[get_current_user] = lambda: user.user_id
    response = client.get("/tasks/view/status",
                          params={
                              "status": task.status.value
                          })

    assert response.status_code == 200
    assert "tasks" in response.json()


def test_view_status_404(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id
    response = client.get("/tasks/view/status",
                          params={
                              "status": "RUNNING"
                          })

    assert response.status_code == 404
    assert response.json()["detail"] == "There are no tasks"


def test_view_priority_200(client, user, task):
    app.dependency_overrides[get_current_user] = lambda: user.user_id
    response = client.get("/tasks/view/priority",
                          params={
                              "priority": task.priority.value
                          })

    assert response.status_code == 200
    assert "tasks" in response.json()


def test_view_priority_404(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id
    response = client.get("/tasks/view/priority",
                          params={
                              "priority": "LOW"
                          })

    assert response.status_code == 404
    assert response.json()["detail"] == "There are no tasks"


def test_get_tasks(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get("/tasks/filter")

    assert response.status_code == 200
    assert "tasks" in response.json()

@pytest.mark.parametrize("sort_by", [
    "created_at",
    "priority",
    "status",
    "title"
])
def test_get_tasks_valid_sort(client, user, sort_by):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(f"/tasks/filter?sort_by={sort_by}")

    assert response.status_code == 200


@pytest.mark.parametrize("order", ["asc", "desc"])
def test_get_tasks_valid_order(client, user, order):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(f"/tasks/filter?order={order}")

    assert response.status_code == 200


@pytest.mark.parametrize("sort_by", ["name", "123", ""])
def test_get_tasks_invalid_sort(client, user, sort_by):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(f"/tasks/filter?sort_by={sort_by}")

    assert response.status_code == 422


@pytest.mark.parametrize("order", ["up", "down"])
def test_get_tasks_invalid_order(client, user, order):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(f"/tasks/filter?order={order}")

    assert response.status_code == 422


@pytest.mark.parametrize("sort_by,order", [
    ("created_at", "asc"),
    ("priority", "desc"),
    ("status", "asc"),
])
def test_get_tasks_2para(client, user, sort_by, order):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(
        f"/tasks/filter?sort_by={sort_by}&order={order}"
    )

    assert response.status_code == 200


@pytest.mark.parametrize("priority,status", [
    ("LOW", "PENDING"),
    ("HIGH", "COMPLETED"),
])
def test_prio_stat_priority_and_status(client, user, priority, status):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(f"/tasks/prio_stat?priority={priority}&status={status}")

    assert response.status_code == 200
    assert "tasks" in response.json()


@pytest.mark.parametrize("priority", ["LOW", "MEDIUM", "HIGH"])
def test_prio_stat_priority_only(client, user, priority):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(f"/tasks/prio_stat?priority={priority}")

    assert response.status_code == 200


@pytest.mark.parametrize("status", ["PENDING", "RUNNING", "COMPLETED"])
def test_prio_stat_status_only(client, user, status):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(f"/tasks/prio_stat?status={status}")

    assert response.status_code == 200


def test_prio_stat_empty(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.get("/tasks/prio_stat?priority=LOW")

    data = response.json()

    assert response.status_code == 200
    assert data["tasks"] == []


@pytest.mark.parametrize("status", ["WRONG", "DONE"])
def test_prio_stat_invalid_status(client, user, status):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get(f"/tasks/prio_stat?status={status}")

    assert response.status_code == 422


def test_update_task_200(client, user, task):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.patch(
        f"/tasks/{task.task_id}",
        json={
            "title": "new title",
            "description": "new desc"
        }
    )

    assert response.status_code == 200


def test_update_task_user_not_found(client, task):
    app.dependency_overrides[get_current_user] = lambda: 0

    response = client.patch(
        f"/tasks/{task.task_id}",
        json={"title": "test"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_tasks_task_not_found(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.patch(
        "/tasks/0",
        json={"title": "test"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_403(client, task, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.patch(
        f"/tasks/{task.task_id}",
        json={"title": "test"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to update task"


def test_delete_all_task_200(client, user, task):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.delete("/tasks/all")

    assert response.status_code == 200
    assert response.json()["message"] == "All tasks deleted successfully"


def test_delete_all_task_404(client, user ):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.delete("/tasks/all")

    assert response.status_code == 404
    assert response.json()["detail"] == "There are no tasks"


def test_delete_task_200(client, user, task):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.delete(f"/tasks/{task.task_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


def test_delete_task_404(client, user ):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.delete("/tasks/0")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task_403(client, admin, task ):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.delete(f"/tasks/{task.task_id}")

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to delete task"


def test_search_task_200(client, task, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get("/tasks/search", params={"key": "test"})

    assert response.status_code == 200
    assert len(response.json()["tasks"]) > 0
    assert "total_tasks" in response.json()


def test_view_all_tasks_200(client, admin, task_for_admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.get("/tasks/view_all_tasks")

    assert response.status_code == 200
    assert "tasks" in response.json()


def test_search_task_404(client, user):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get("/tasks/search", params={"key": "nothing"})

    assert response.json()["status_code"] == 404
    assert response.json()["message"] == "No matching tasks found"



def test_view_all_tasks_404(client, admin):
    app.dependency_overrides[get_current_user] = lambda: admin.user_id

    response = client.get("/tasks/view_all_tasks")

    assert response.status_code == 404
    assert response.json()["detail"] == "No tasks found"


def test_view_all_tasks_user_not_found_404(client):
    app.dependency_overrides[get_current_user] = lambda: 0

    response = client.get("/tasks/view_all_tasks")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_view_all_tasks_403(client, user, task):
    app.dependency_overrides[get_current_user] = lambda: user.user_id

    response = client.get("/tasks/view_all_tasks")

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to view tasks"
