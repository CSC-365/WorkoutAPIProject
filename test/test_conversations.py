from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


"""
json boiler plate 

{
  "character_1_id": 0,
  "character_2_id": 0,
  "lines": [
    {
      "character_id": 0,
      "line_text": "string"
    }
  ]
}
"""
# make sure this fails when the movie doesn't exist
def test_add_conversations00():
    # there is no movie with 100

  testJson = {
              "character_1_id": 0,
              "character_2_id": 1,
              "lines": [
                  {
                  "character_id": 0,
                  "line_text": "error"
                  }
              ]
          }

  response = client.post("/movies/100/conversations/", json = testJson)
  assert response.status_code == 404

  with open("test/conversations/movie_not_found.json") as f:
      assert response.json() == json.load(f)

# test that the character is part of the given movie
def test_add_conversations01():
  # characters 5558 and 5559 are not in movie 371, they are in movie 369
  testJson = {
              "character_1_id": 5558,
              "character_2_id": 5559,
              "lines": [
                  {
                  "character_id": 5559,
                  "line_text": "error"
                  }
              ]
          }

  response = client.post("/movies/371/conversations", json = testJson)
  assert response.status_code == 400

  with open("test/conversations/not_in_movie.json") as f:
      assert response.json() == json.load(f)


# test that the characters are not the same
def test_add_conversations02():
  # characters 6055 and 6055 are the same characters
  testJson = {
              "character_1_id": 6055,
              "character_2_id": 6055,
              "lines": [
                  {
                  "character_id": 6055,
                  "line_text": "error"
                  }
              ]
          }

  response = client.post("/movies/402/conversations", json = testJson)
  assert response.status_code == 400

  with open("test/conversations/same_characters.json") as f:
      assert response.json() == json.load(f)
   
# test tha the lines match the characters
# def test_add_conversations03():
#   # characters 0 and 11 are in movie 0, but the line has an invalid id
#   testJson = {
#               "character_1_id": 0,
#               "character_2_id": 11,
#               "lines": [
#                   {
#                   "character_id": 6055,
#                   "line_text": "error"
#                   }
#               ]
#           }

#   response = client.post("/movies/0/conversations", json = testJson)
#   assert response.status_code == 400

#   with open("test/conversations/lines_dont_match.json") as f:
#       assert response.json() == json.load(f)

# # check that old endpoints work after the conversation gets added test1
# # adding a coversation between apoc and oracle from the matrix and then testing my /lines/names/{name} endpoints
# def test_add_conversations04():
#   testJson = {
#               "character_1_id": 6518,
#               "character_2_id": 6524,
#               "lines": [
#                   {
#                   "character_id": 6518,
#                   "line_text": "hey oracle, did you know the warriors used to play there?"
#                   },
#                   {
#                   "character_id": 6524,
#                   "line_text": "yeah but now they play at chase"
#                   },
#                   {
#                   "character_id": 6518,
#                   "line_text": "i feel bad everyone is leaving oakland"
#                   },
#                   {
#                   "character_id": 6524,
#                   "line_text": "eh its alright, the raiders suck anyways"
#                   },
#                   {
#                   "character_id": 6518,
#                   "line_text": "bang bang niner gang baby oracle"
#                   }

#               ]
#           }
  
#   response = client.post("/movies/433/conversations", json = testJson)
#   assert response.status_code == 200

#   # check that the endpoint still works after adding the conversation
#   response = client.get("/lines/names/apoc")
#   assert response.status_code == 200

#   with open("test/conversations/apoc.json") as f:
#       assert response.json() == json.load(f)

#   response = client.get("/lines/83074")
#   assert response.status_code == 200

#   with open("test/conversations/83074.json") as f:
#       assert response.json() == json.load(f)

# check that old endpoints work after the conversation gets added test2
def test_add_conversations05():
  # testJson = {
  #             "character_1_id": 7056,
  #             "character_2_id": 7060,
  #             "lines": [
  #               {
  #                  "character_id": 7056,
  #                   "line_text": "what a wonderful day in the library it is"
  #               }
  #             ]
  # }

  # response = client.post("/movies/472/conversations", json = testJson)
  # assert response.status_code == 200

  # checking previous endpoints

  response = client.get("/lines/names/imam")
  assert response.status_code == 200


  with open("test/conversations/imam.json") as f:
      assert response.json() == json.load(f)




