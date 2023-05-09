from fastapi.testclient import TestClient
from src.api.server import app
import json
client = TestClient(app)

def test_workout():
    response = client.get("/workouts/1")
    assert response.status_code == 200
    with open('test/workouts/1.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_workout2():
    response = client.get("/workouts/2")
    assert response.status_code == 200
    with open('test/workouts/2.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)