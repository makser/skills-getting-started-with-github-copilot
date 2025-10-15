import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/remove", params={"email": email})
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try duplicate signup
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 400
    # Remove again
    response3 = client.post(f"/activities/{activity}/remove", params={"email": email})
    assert response3.status_code == 200
    assert f"Removed {email}" in response3.json()["message"]

def test_remove_nonexistent_participant():
    response = client.post("/activities/Chess Club/remove", params={"email": "notfound@mergington.edu"})
    assert response.status_code == 404

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
