import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_read_task(client: AsyncClient):
    # 1. Inscription et Connexion
    register_payload = {
        "email": "taskuser@example.com",
        "password": "Password123!",
        "full_name": "Task Tester"
    }
    await client.post("/api/v1/auth/register", json=register_payload)
    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "taskuser@example.com", "password": "Password123!"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Création de tâche
    task_payload = {
        "title": "Tâche de test automatisé",
        "description": "Description de la tâche",
        "status": "PENDING",
        "priority": "HIGH"
    }
    create_res = await client.post("/api/v1/tasks/", json=task_payload, headers=headers)
    assert create_res.status_code == 201
    task_data = create_res.json()
    assert task_data["title"] == "Tâche de test automatisé"
    task_id = task_data["id"]

    # 3. Lecture des tâches avec filtrage
    get_res = await client.get("/api/v1/tasks/?status=PENDING", headers=headers)
    assert get_res.status_code == 200
    tasks_list = get_res.json()
    assert len(tasks_list) == 1
    assert tasks_list[0]["id"] == task_id

    # 4. Suppression de la tâche
    del_res = await client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert del_res.status_code == 204
