from fastapi.testclient import TestClient
from src.api.server import app
import json
client = TestClient(app)


def test_get_log():
    response = client.get("/user/1/logs")
    assert response.status_code == 200
    with open('test/logs/1.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_log2():
    response = client.get("/user/15/logs")
    assert response.status_code == 200
    with open('test/logs/15.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_create_log():
    response = client.post("/user/11/logs", json=
        {
        "current_lbs": 80
        }
    )
    assert response.status_code == 200

def test_create_log2():
    response = client.post("/user/12/logs", json=
        {
        "current_lbs": 80
        }
    )
    assert response.status_code == 200

