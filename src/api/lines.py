from fastapi import APIRouter, HTTPException
from enum import Enum 
from src import database as db
from typing import *
from sqlalchemy import *

router = APIRouter()


"""
functions for lines.py
list conversation -> display all of the lines of a conversation 
write out the first line of each conversation character is part of (searched by character name)

"""

@router.get("/lines/{conversation_id}", tags=["lines"])
def get_lines(conversation_id: int):
    """
    This endpoint returns the lines of a conversation based on its id. For each conversation, the endpoint returns
    * 'conversation_id': the conversation id of your desired conversation
    * 'title': the title of the movie the conversation is from
    * 'lines': a list of lines in the given conversation, sorted in order of line_sort
    
    Each line is represented with the following keys
    * 'name': the name of the character who said the line
    * 'line_text': the text of the line
    
    """

    json = None

    with db.engine.connect() as conn:
        convo = conn.execute(text("SELECT * FROM conversations WHERE conversation_id = :id"), {"id":conversation_id}).fetchone()
        if convo:
            lines = conn.execute(text("SELECT l.*, c.name FROM lines AS l JOIN characters AS c ON l.character_id = c.character_id WHERE l.conversation_id = :id ORDER BY line_sort"), {"id":conversation_id}).fetchall()
            json = {
                "conversation_id": conversation_id,
                "title": conn.execute(text("SELECT title FROM movies WHERE movie_id = :id"), {"id":convo.movie_id}).fetchone().title,
                "lines": [{
                    "name": line.name,
                    "line_text": line.line_text
                } for line in lines]
            }
    
    if json is None:
        raise HTTPException(status_code=404, detail="conversation not found.")

    return json

    if conversation_id in db.conversations:

        lines = [(line, db.characters[line.character_id].name) for line in db.lines.values() if conversation_id == line.conversation_id]

        # sort for outputting
        lines = sorted(lines, key=lambda x: x[0].line_sort)

        lineJson = [{
            "name": line[1],
            "line_text": line[0].line_text
        } for line in lines]

        json = {
            "conversation_id": conversation_id,
            "title": db.movies[db.conversations[conversation_id].movie_id].title,
            "lines": lineJson
        }

        if json is None:
            raise HTTPException(status_code=404, detail="conversation not found.")
        
        return json
    
@router.get("/lines/names/{name}", tags=["lines"])
def get_character_convos(name: str):
    """
    This endpoint returns a list of characters that match the given name. For each character, the endpoint returns:
    * 'name': The character's name
    * 'character_id': character id 
    * 'conversation count': amount of conversations the character is in
    * 'conversations': a list of conversations the character is in, sorted by conversation id

    Each conversation identifier is represented by a dictionary with the following keys:
    * 'title': Movie title the character is in
    * 'line_count': how many lines the character had in the conversation
    * 'other_charcter': the name of the other character they are talking to
    """
    jsons = []
    name = name.upper()
    with db.engine.connect() as conn:
        chars = conn.execute(text("SELECT * FROM characters WHERE name = :name"), {"name":name}).fetchall()
        if chars != []:
            for char in chars:
                convos = conn.execute(text("SELECT * FROM conversations WHERE character1_id = :id OR character2_id = :id"), {"id":char.character_id}).fetchall()
                json = {
                    "name": name,
                    "character_id": char.character_id,
                    "conversation_count": len(convos),
                    "conversations": [{
                        "title": conn.execute(text("SELECT title FROM movies WHERE movie_id = :id"), {"id":convo.movie_id}).fetchone().title,
                        "line_count": conn.execute(text("SELECT COUNT(*) FROM lines AS l WHERE l.character_id = :character1_id AND l.conversation_id = :conversation_id"), {"character1_id": convo.character1_id, "conversation_id": convo.conversation_id}).fetchone()[0] if convo.character1_id == char.character_id else conn.execute(text("SELECT COUNT(*) FROM lines AS l WHERE l.character_id = :character2_id AND l.conversation_id = :conversation_id"),{"character2_id": convo.character2_id, "conversation_id": convo.conversation_id}).fetchone()[0],
                        "other_character": conn.execute(text("SELECT name FROM characters WHERE character_id = :id"), {"id":convo.character2_id if convo.character1_id == char.character_id else convo.character1_id}).fetchone().name
                    } for convo in convos]
                }
                jsons.append(json)
    
    if jsons == []:
        raise HTTPException(status_code=404, detail="character not found.")
    
    return jsons
    jsons = []

    name = name.upper()     # turn the name into all caps in order to match the datab

    if name in db.charNames:
        for id in db.charNames[name]:
            convos = [] #[convo for convo in data.conversations.values() if convo.character1_id == id or convo.character2_id == id]

            # convo to keep only one of each conversation
            c = {}
            for convo in db.conversations.values():
                if (convo.character1_id == id or convo.character2_id == id) and convo.conversation_id not in c:
                    convos.append(convo)
            
            convos = sorted(convos, key=lambda x: x.conversation_id)

            convosJson = []

            for convo in convos:
                if id == convo.character1_id:
                    count = convo.character1_lines
                    other = db.characters[convo.character2_id].name
                else:
                    count = convo.character2_lines
                    other = db.characters[convo.character1_id].name

                convosJson.append({
                    "title": db.movies[convo.movie_id].title,
                    "line_count": count,
                    "other_character": other
                }) 

            json ={
                "name": name,
                "character_id": id,
                "conversation_count": len(convos),
                "conversations": convosJson
            }
            jsons.append(json)
    
    # this means that the name was not found
    if jsons == []:
        raise HTTPException(status_code=404, detail="character not found.")

    return jsons

class conversation_sort_options(str, Enum):
    line_count = "line_count"
    title = "title"
    conversation_id = "conversation_id"

@router.get("/lines/conversations/", tags=["lines"])
def list_conversations(
    count: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
    sort: conversation_sort_options = conversation_sort_options.conversation_id
):
    """
    This endpoint returns a list of conversations. For each conversation it returns:
    * 'conversation_id': the internal id of the  conversation
    * 'title': title of the movie it is from
    * 'character1': character1's name
    * 'character2': character2's name
    * 'line_count': line count for conversation

    You can filter for conversations whose conversations only meet the lineCount
    threshold

    You can sort the results by using the 'sort' query parameter:
    * 'line_count' - Sort based on line count, descending
    * 'title' - alphabetically sorted 
    * 'conversation_id' sorted based on conversation id's
    """
    json = None
    metadata = MetaData()
    conversations = Table("conversations", metadata, autoload_with=db.engine)
    lines = Table("lines", metadata, autoload_with=db.engine)
    movies = Table("movies", metadata, autoload_with=db.engine)


    query = conversations.join(movies, conversations.c.movie_id == movies.c.movie_id).join(lines, conversations.c.conversation_id == lines.c.conversation_id).select().with_only_columns(conversations.c.conversation_id, movies.c.title, conversations.c.character1_id, conversations.c.character2_id, func.count(lines.c.line_id).label("line_count"))

    query = query.group_by(conversations.c.conversation_id, movies.c.title, conversations.c.character1_id, conversations.c.character2_id)
    if count is not None:
        query = query.having(func.count(lines.c.line_id) >= count)

    if sort == conversation_sort_options.conversation_id:
        query = query.order_by(conversations.c.conversation_id).limit(limit).offset(offset)
    elif sort == conversation_sort_options.title: 
        query = query.order_by(movies.c.title).limit(limit).offset(offset)
    elif sort == conversation_sort_options.line_count:
        query = query.order_by(desc("line_count")).limit(limit).offset(offset)

    

    with db.engine.connect() as conn:
        print(query)
        convos = conn.execute(query).fetchall()
        json = [{
            "conversation_id": convo.conversation_id,
            "title": convo.title,
            "character1": conn.execute(text("SELECT name FROM characters WHERE character_id = :id"), {"id": convo.character1_id}).fetchone().name,
            "character2": conn.execute(text("SELECT name FROM characters WHERE character_id = :id"), {"id": convo.character2_id}).fetchone().name,
            "line_count": convo[4]
        } for convo in convos]


    return json
    if count:
        convos = [convo for convo in db.conversations.values() if convo.lineCount >= count]
    else:
        convos = [convo for convo in db.conversations.values()]

    if sort == conversation_sort_options.line_count:
        convos = sorted(convos, key=lambda x: x.lineCount, reverse=True)
    elif sort == conversation_sort_options.title:
        convos = sorted(convos, key = lambda x: db.movies[x.movie_id].title)
    elif sort == conversation_sort_options.conversation_id:
        convos = sorted(convos, key=lambda x: x.conversation_id)

    json = []

    # TODO: make sure it doesn't go more than the list

    for convo in convos[offset:offset + limit]:
        print(vars(convo))
        convoJson = {
            "conversation_id": convo.conversation_id,
            "title": db.movies[convo.movie_id].title,
            "character1": db.characters[convo.character1_id].name,
            "character2": db.characters[convo.character2_id].name,
            "line_count": convo.lineCount
        }
        json.append(convoJson)


    # for i in range(offset, limit + offset):
    #     convoJson = {
    #         "conversation_id": convos[i].conversation_id,
    #         "title": data.movies[convos[i].movie_id].title,
    #         "character1": data.characters[convos[i].character1_id].name,
    #         "character2": data.characters[convos[i].character2_id].name,
    #         "line_count": convos[i].lineCount
    #     }
    #     json.append(convoJson)

    return json

#@router.get("/characters/{id}", tags=["characters"])

