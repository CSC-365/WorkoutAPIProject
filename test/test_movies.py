from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_movie():
    response = client.get("/movies/44")
    assert response.status_code == 200

    with open("test/movies/44.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_movies():
    response = client.get("/movies/")
    assert response.status_code == 200

    with open("test/movies/root.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

# New test case
def test_get_movie2():
    # tests null character in top characters
    response = client.get("/movies/436")
    assert response.status_code == 200

    with open("test/movies/436.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_sort_filter():
    response = client.get("/movies/?name=big&limit=50&offset=0&sort=rating")
    assert response.status_code == 200

    with open(
        "test/movies/movies-name=big&limit=50&offset=0&sort=rating.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)

# testing sorting with with movies with the word fast 
# only 5 of them sorted by title
def test_02():
    response= client.get("/movies/?name=man&limit=5&offset=0&sort=movie_title")
    assert response.status_code == 200

    with open(
        "test/movies/movies-name=man&limit=5&offset=0&sort=movie_title.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)

# test for movie with id = 497
def test_03():
    response = client.get("/movies/497")
    assert response.status_code == 200

    with open("test/movies/497.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_404():
    response = client.get("/movies/1")
    assert response.status_code == 404
