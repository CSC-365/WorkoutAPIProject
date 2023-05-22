from fastapi.testclient import TestClient
from src.api.server import app
import json
client = TestClient(app)

def test_get_projection():
    response = client.get("/user/11/projection")
    assert response.status_code == 200
    with open('test/projection/11.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_create_projection():
    response = client.post("/user/11/projection", json={
    "projection_date": "2023-07-22"
    })
    assert response.status_code == 200  

def test_get_projection2():
    response = client.get("/user/1/projection")
    assert response.status_code == 200
    with open('test/projection/1.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_create_projection2():
    response = client.post("/user/1/projection", json={
    "projection_date": "2023-07-25"
    })
    assert response.status_code == 200