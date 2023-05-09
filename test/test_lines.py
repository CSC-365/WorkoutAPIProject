from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_lines():
    response = client.get("/lines/1")
    assert response.status_code == 200

    with open("test/lines/1.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
def test_get_lines2():
    response = client.get("/lines/2")
    assert response.status_code == 200

    with open("test/lines/2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_conversations():
    response = client.get("/lines/2/conversations")
    assert response.status_code == 200

    with open("test/lines/conv2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_conversations2():
    response = client.get("/lines/4/conversations")
    assert response.status_code == 200

    with open("test/lines/conv4.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_longest_lines():
    response = client.get("/lines/longest/1?limit=1&offset=2")
    assert response.status_code == 200

    with open("test/lines/lines1Lim=1Off=2", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_404():
    response = client.get("/lines/400")
    assert response.status_code == 404
