import pytest
from httpx import AsyncClient
from src.app import app
from fastapi.testclient import TestClient

# Arrange-Act-Assert (AAA) pattern is used in all tests

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange: create async test client
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: call the GET /activities endpoint
        response = await ac.get("/activities")
    # Assert: check response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

@pytest.mark.asyncio
async def test_signup_for_activity():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: sign up the test user
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json().get("message", "")
    # Confirm user is in participants
    get_resp = await ac.get("/activities")
    assert test_email in get_resp.json()[activity]["participants"]
