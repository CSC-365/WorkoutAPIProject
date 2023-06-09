from fastapi.testclient import TestClient
from src.api.server import app
client = TestClient(app)


def test_create_goal():
    response = client.post("/goals/", json={
        "user_id": 4,
        "type_id": 0,
        "target_weight": 150
    })
    assert response.status_code == 200
    # no other way to test since we don't have a get goal endpoint
def test_create_goal2():
    response = client.post("/goals/", json={
        "user_id": 5,
        "type_id": 0,
        "target_weight": 150
    })
    assert response.status_code == 200

