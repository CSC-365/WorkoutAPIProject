from fastapi.testclient import TestClient
from src.api.server import app
import json
client = TestClient(app)


def test_create_user():
    response = client.post("/users/", json=
        {
            "username": "test",
            "password": "test1",
            "starting_lbs": 100,
            "height_inches": 78,
            "avg_calorie_intake": 2400,
            "birthday": "1978-04-03",
            "gender": "M"
        }
    )

    
    assert response.status_code == 200

def test_create_user2():
    response = client.post("/users/", json=
        {
            "username": "test2",
            "password": "test2",
            "starting_lbs": 300,
            "height_inches": 88,
            "avg_calorie_intake": 3000,
            "birthday": "2000-01-23",
            "gender": "M"
        }
    )
    
    assert response.status_code == 200

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    with open('test/users/1.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_user2():
    response = client.get("/users/2")
    assert response.status_code == 200
    with open('test/users/2.json', encoding="utf-8") as f:
        assert response.json() == json.load(f)