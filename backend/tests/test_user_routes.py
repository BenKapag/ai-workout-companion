import sys
import os

# Ensure we can import from the backend folder when running pytest
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from unittest.mock import AsyncMock
from routers.user_routes import hash_password  # Correct import


# Fixture: Reusable test client using FastAPI's in-memory ASGI transport
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# Test: Register a new user (happy path)
@pytest.mark.asyncio
async def test_register_success(client, mocker):
    """
    Simulates a successful registration by mocking the DB microservice call.
    """
    mock_response = mocker.AsyncMock()
    mock_response.status_code = 201
    mock_response.json = AsyncMock(return_value={"user_id": 1, "username": "testUser"})

    mocker.patch(
        "backend.routers.user_routes.httpx.AsyncClient.post",
        return_value=mock_response
    )

    response = await client.post("/register", json={
        "username": "testUser",
        "password": "securepass"
    })

    assert response.status_code == 201
    json_body = await response.json()
    assert json_body["username"] == "testUser"


# Test: Login success
@pytest.mark.asyncio
async def test_login_success(client, mocker):
    """
    Simulates a successful login and verifies that the token is returned.
    """
    mock_response = mocker.AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={
        "id": 1,
        "username": "testUser",
        "hashed_password": hash_password("securepass")
    })

    mocker.patch(
        "backend.routers.user_routes.httpx.AsyncClient.get",
        return_value=mock_response
    )

    response = await client.post("/login", json={
        "username": "testUser",
        "password": "securepass"
    })

    assert response.status_code == 200
    json_body = response.json()  #  No await — mock returns dict directly
    assert "token" in json_body


# Test: Get profile (auth success and DB success)
@pytest.mark.asyncio
async def test_get_profile_success(client, mocker):
    """
    Mocks the GET /users/{id}/profile DB call and verifies the backend returns it.
    """
    mocker.patch(
        "backend.services.auth_dependency.get_current_user",
        return_value={"id": 1, "username": "testUser"}
    )

    mock_response = mocker.AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={
        "age": 28,
        "goal": "gain muscle",
        "experience_level": "intermediate"
    })

    mocker.patch(
        "backend.services.db_service.httpx.AsyncClient.get",
        return_value=mock_response
    )

    response = await client.get("/profile")

    assert response.status_code == 200
    json_body = await response.json()
    assert json_body["goal"] == "gain muscle"
