from collections import defaultdict
from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
from sqlalchemy import *

from fastapi.params import Query
from src import database as db

router = APIRouter()


@router.get("/characters/{id}", tags=["characters"])
def get_character(id: int):
    """
    This endpoint returns a single character by its identifier. For each character
    it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `gender`: The gender of the character.
    * `top_conversations`: A list of characters that the character has the most
      conversations with. The characters are listed in order of the number of
      lines together. These conversations are described below.

    Each conversation is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * `number_of_lines_together`: The number of lines the character has with the
      originally queried character.
    """

    # TODO: Implement the endpoint using sql 
    # for conversations
        # query to get all the conversations the character is part of 

    json = None
    with db.engine.connect() as conn:
        character = conn.execute(text("SELECT * FROM characters WHERE character_id = :id"), {"id":id}).fetchone()
        if character:
            convos = conn.execute(text("SELECT char.character_id, char.name, char.gender, mov.title, SUM(c.line_count) as count FROM (SELECT c.conversation_id, c.movie_id, CASE WHEN c.character1_id = :id THEN c.character2_id ELSE c.character1_id END AS other_character_id, COUNT(l.line_id) AS line_count FROM conversations AS c JOIN lines AS l on c.conversation_id = l.conversation_id WHERE (c.character1_id = :id OR c.character2_id = :id) AND (c.character1_id != :id OR c.character2_id != :id) GROUP BY c.conversation_id, c.movie_id, other_character_id) AS c JOIN characters AS char ON c.other_character_id = char.character_id JOIN movies AS mov on c.movie_id = mov.movie_id GROUP BY char.character_id, char.name, char.gender, mov.title ORDER BY SUM(c.line_count) DESC"), {"id": id}).fetchall()
            cJson = []
            for convo in convos:
                cur = {
                    "character_id": convo.character_id,
                    "character": convo.name,
                    "gender": convo.gender,
                    "number_of_lines_together": convo.count
                }
                cJson.append(cur)

            json = {
                "character_id": character.character_id,
                "character": character.name,
                "movie": conn.execute(text("SELECT * FROM movies WHERE movie_id = :id"), {"id":character.movie_id}).fetchone().title,
                "gender": character.gender,
                "top_conversations": cJson
            }
    if json is None:
        raise HTTPException(status_code=404, detail="character not found.")
    return json

    json = None
    # print(data.characters)


    # remove this just lookup in the dictionary
    # if character exists
    if id in db.characters:
        print("character found")
        character = db.characters[id]

        """
        convo_json strats:

        traverse the conversations
          for each conversation, we traverse the lines file to calculate the amount of lines & such
        """
        
        convos = defaultdict(int)
        convosJson = []

        # for the character, traverse through the conversations and add the convo object if the have a convo
        # sort them based on the conversation lineCount
        for convo in db.conversations.values():
            if convo.character1_id == character.character_id:
                # add the object based on the second character
                convos[convo.character2_id] += convo.lineCount
            elif convo.character2_id == character.character_id:
                convos[convo.character1_id] += convo.lineCount
        convosSorted = sorted(convos.items(), key=lambda x: x[1], reverse=True)

        # after the list is made, turn them all into json's for the return statement
        for convo in convosSorted:
            
            convoJson = {
                "character_id": convo[0],
                "character": db.characters[convo[0]].name,
                "gender": db.characters[convo[0]].gender,
                "number_of_lines_together": convo[1]
            }
            convosJson.append(convoJson)

        # building the actual character json
        json = {
            "character_id": character.character_id,
            "character": character.name,
            "movie": db.movies[character.movie_id].title,
            "gender": character.gender,
            "top_conversations": convosJson
          }
    if json is None:
        raise HTTPException(status_code=404, detail="character not found.")
    return json


class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"


@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: character_sort_options = character_sort_options.character,
):
    """
    This endpoint returns a list of characters. For each character it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `number_of_lines`: The number of lines the character has in the movie.

    You can filter for characters whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    * `number_of_lines` - Sort by number of lines, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    metadata = MetaData()
    characters = Table("characters", metadata, autoload_with=db.engine)
    movies = Table("movies", metadata, autoload_with=db.engine)
    lines = Table("lines", metadata, autoload_with=db.engine)   # used to calculate the number of lines

    
    if sort == character_sort_options.character:
        s = characters.c.name
    elif sort == character_sort_options.movie:
        s = movies.c.title
    elif sort == character_sort_options.number_of_lines:
        s = desc("line_count")
    query = characters.join(lines, characters.c.character_id == lines.c.character_id).join(movies, characters.c.movie_id == movies.c.movie_id).select().with_only_columns(characters.c.character_id, characters.c.name, characters.c.movie_id, func.count(lines.c.line_id).label("line_count"), movies.c.title).group_by(characters.c.character_id, movies.c.title)
    if name != "":
        query = query.where(characters.c.name.ilike(f"%{name}%"))

    query = query.order_by(s, characters.c.character_id).limit(limit).offset(offset)
    
    with db.engine.connect() as conn:
        result = conn.execute(query).fetchall()
        json = []
        for row in result:
            cur = {
                "character_id": row.character_id,
                "character": row.name,
                "movie": row.title,
                "number_of_lines": row.line_count
            }
            json.append(cur)

    return json
    # filter out
    if name != "":
      charList = [character for character in db.characters.values() if name.upper() in character.name]
    else:
      charList = [character for character in db.characters.values() if character.name is not None]
        
    # in order to preprocess the number of lines, I am going to have one pass through the 
    if sort == character_sort_options.character:
        charList = sorted(charList, key=lambda x: x.name)
        
        
    elif sort == character_sort_options.movie:
        charList = sorted(charList, key=lambda x: x.movie)

    elif sort == character_sort_options.number_of_lines:
        charList = sorted(charList, key=lambda x: x.lines, reverse=True)

    json = []

    # making sure the limit isn't too high
    if limit > len(charList):
        limit = len(charList)


    for character in charList[offset: offset + limit]:
        characterJson = {
            "character_id": character.character_id,
            "character": character.name,
            "movie": db.movies[character.movie_id].title,
            "number_of_lines": character.lines
        }
        json.append(characterJson)

    # for i in range(offset, offset + limit):
    #     characterJson = {
    #         "character_id": charList[i].character_id,
    #         "character": charList[i].name,
    #         "movie": data.movies[charList[i].movie_id].title,
    #         "number_of_lines": charList[i].lines
    #     }
    #     json.append(characterJson)
    return json
