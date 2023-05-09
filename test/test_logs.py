from fastapi.testclient import TestClient
from src.api.server import app
import json
client = TestClient(app)


def test_get_log():
    response = client.get("/logs/1")
    assert response.status_code == 200
    with open('test/logs/1.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_log2():
    response = client.get("/logs/15")
    assert response.status_code == 200
    with open('test/logs/15.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_create_log():
    response = client.post("/logs/", json=
        {
        "user_id": 11,
        "current_lbs": 80
        }
    )
    assert response.status_code == 200

def test_create_log2():
    response = client.post("/logs/", json=
        {
        "user_id": 12,
        "current_lbs": 80
        }
    )
    assert response.status_code == 200

