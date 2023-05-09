from fastapi.testclient import TestClient

from src.api.server import app

import json


client = TestClient(app)

def test_add_conversation():
    lines_response = client.get("/lines/10")
    response = client.post("/movies/0/conversations/", json={
        "character_1_id": 10,
        "character_2_id": 11,
        "lines": [
            {
                "character_id": 10,
                "line_text": "I'm a line!"
            },
            {
                "character_id": 11,
                "line_text": "I'm a line too!"
            }
        ]
    })
    lines_response_2 = client.get("/lines/10")
    assert response.status_code == 200
    assert lines_response != lines_response_2

def test_add_conversation2():
    lines_response = client.get("/lines/49/conversations/")
    response = client.post("/movies/3/conversations/", json={
        "character_1_id": 49,
        "character_2_id": 50,
        "lines": [
            {
                "character_id": 49,
                "line_text": "I'm a line! This is my second test!"
            },
            {
                "character_id": 50,
                "line_text": "I'm a line too! This is my second test!"
            }
        ]
    })
    lines_response_2 = client.get("/lines/49/conversations/")
    assert response.status_code == 200
    assert lines_response != lines_response_2