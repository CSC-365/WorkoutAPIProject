from fastapi.testclient import TestClient

from src.api.server import app


import json



client = TestClient(app)

def test_workout():
    response = client.get("/workouts/1")
    assert response.status_code == 200
    with open('test/test_workouts.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)
    