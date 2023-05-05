from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_lines0():
    response = client.get("/lines/2619")
    assert response.status_code == 200

    with open("test/lines/2619.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_lines1():
    response = client.get("/lines/6123")
    assert response.status_code == 200

    with open("test/lines/6123.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_list_conversations0():
    response = client.get("/lines/names/FERRARI")
    assert response.status_code == 200

    with open("test/lines/FERRARI.json") as f:
        print(response.json())
        assert response.json() == json.load(f)

def test_list_conversations1():
    response = client.get("/lines/names/KEN")
    assert response.status_code == 200

    with open("test/lines/KEN.json") as f:
        assert response.json() == json.load(f)

def test_list_conversations2():
    response = client.get("/lines/names/BIANCA")
    assert response.status_code == 200

    with open("test/lines/BIANCA.json") as f:
        assert response.json() == json.load(f)

def test_list_conversations3():
    response = client.get("/lines/names/bianca")
    assert response.status_code == 200

    with open("test/lines/bianca.json") as f:
        assert response.json() == json.load(f)

def test_lines0():
    response = client.get("/lines/conversations/?count=25&limit=15&sort=line_count")
    assert response.status_code == 200

    with open("test/lines/lines-count=25&limit=15&sort=line_count.json") as f:
        assert response.json() == json.load(f)

def test_lines1():
    response = client.get("/lines/conversations/?count=0&offset=3547&limit=25&sort=conversation_id")

    with open("test/lines/lines-count=0&offset=3547&limit=25&sort=conversation_id.json") as f:
        assert response.json() == json.load(f)
