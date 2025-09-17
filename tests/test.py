import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status

from src.main import app

base_url = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_create_note():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        payload = {
            "title": "Test Note",
            "content": "This is a test note",
            "user_id": 1,
            "tag_ids": [0],
        }

        token = await get_token(ac)
        headers = {"Authorization": f"Bearer {token}"}

        response = await ac.post("/note/", json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data["note"]
    assert data["note"]["title"] == "Test Note"


@pytest.mark.asyncio
async def test_get_note():
    note_id = 12
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        token = await get_token(ac)
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.get(f"/note/{note_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == note_id
    assert "title" in data


@pytest.mark.asyncio
async def test_update_note():
    note_id = 10
    update_payload = {
        "title": "Updated Note Title",
        "content": "Updated note content",
        "tag_ids": [0],
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        token = await get_token(ac)
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.patch(
            f"/note/{note_id}", json=update_payload, headers=headers
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Note Title"


@pytest.mark.asyncio
async def test_delete_note():
    note_id = 5
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        token = await get_token(ac)
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.delete(f"/note/{note_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK


async def get_token(ac: AsyncClient) -> str:
    response = await ac.post(
        "/user/login", json={"username": "kareem", "password": "kareemkimo"}
    )
    assert response.status_code == 200
    return response.json()["token"]
