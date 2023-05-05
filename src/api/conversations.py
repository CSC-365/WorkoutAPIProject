from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy import *


# FastAPI is inferring what the request body should look like
# based on the following two classes.
class LinesJson(BaseModel):
    character_id: int
    line_text: str


class ConversationJson(BaseModel):
    character_1_id: int
    character_2_id: int
    lines: List[LinesJson]


router = APIRouter()


@router.post("/movies/{movie_id}/conversations/", tags=["movies"])
def add_conversation(movie_id: int, conversation: ConversationJson):
    """
    This endpoint adds a conversation to a movie. The conversation is represented
    by the two characters involved in the conversation and a series of lines between
    those characters in the movie.

    The endpoint ensures that all characters are part of the referenced movie,
    that the characters are not the same, and that the lines of a conversation
    match the characters involved in the conversation.

    Line sort is set based on the order in which the lines are provided in the
    request body.

    The endpoint returns the id of the resulting conversation that was created.

    Limitations:
        1. if someone performs a GET request while information from a POST request were being added to the database from another call, they will not be able to access the data as it is being added
        2. If two POST requests are being processed at the same time, a race condition can occur for attributes such as 'character1_lines' due to the fact that two proceses are trying to modify the attribute at the same time. This will of course end up in inaccurate data
            - this can also occur in terms of the line id as the lines could be out of order and not near other lines of the same conversation
        3. As a result of a race condition, duplicate lines/ conversations can be added to the database
        4. Besides a race condition, there is the limitation of users being able to add the same conversation twice
            - this api does not evaluate whether or not the conversation already exists in the database
        5. A race condition can not only prevent there from being accurate data being displayed, but it can also cause errors such as finding a certain conversation based off its id
            - if the id isn't created yet, then it wont be accessed, causing an error and resulting in the pending api request to fail out

    """

    # TODO:
    # 1. Check that the movie exists
    # 2. Check that the characters exist and are part of the movie
    # 3. Check that the characters are not the same
    # 4. Check that the lines match the characters
    # 5. Create the conversation
    # 6. Create the lines
    # 7. Return the conversation id

    metadata = MetaData()
    convos = Table('conversations', metadata, autoload_with=db.engine)
    lines = Table('lines', metadata, autoload_with=db.engine)

    with db.engine.begin() as conn:
        
        # check 1 - movie exists
        c1 = conn.execute(text("SELECT * FROM movies WHERE movie_id = :id"), {"id":movie_id}).fetchone()
        if c1 is None:
            raise HTTPException(status_code=404, detail="movie not found.")
        
        # check 2 - characters exist and are part of the movie
        c2 = conn.execute(text("SELECT * FROM characters WHERE character_id = :id AND movie_id = :movie_id"), {"id":conversation.character_1_id, "movie_id":movie_id}).fetchone()
        c3 = conn.execute(text("SELECT * FROM characters WHERE character_id = :id AND movie_id = :movie_id"), {"id": conversation.character_2_id, "movie_id":movie_id}).fetchone()
        if c2 is None or c3 is None:
            raise HTTPException(status_code=400, detail="characters not in movie.")
        
        # check 3 - characters are not the same
        if conversation.character_1_id == conversation.character_2_id:
            raise HTTPException(status_code=400, detail="characters are the same.")
        
        # check 4 - lines match the characters
        for line in conversation.lines:
            if line.character_id != conversation.character_1_id and line.character_id != conversation.character_2_id:
                raise HTTPException(status_code=400, detail="line character id does not match given characters.")
            
        # create the conversation
        convo_id = conn.execute(text("SELECT MAX(conversation_id) FROM conversations")).fetchone()[0] + 1
        conn.execute(convos.insert().values(conversation_id=convo_id, character1_id=conversation.character_1_id, character2_id=conversation.character_2_id, movie_id=movie_id))

        # create and add the lines
        for s, line in enumerate(conversation.lines):
            line_id = conn.execute(text("SELECT MAX(line_id) FROM lines")).fetchone()[0] + 1
            conn.execute(lines.insert().values(line_id=line_id, character_id=line.character_id, movie_id=movie_id, conversation_id=convo_id, line_sort=s, line_text=line.line_text))
    return convo_id
    # checking that the movie exists
    if movie_id not in db.movies:
        raise HTTPException(status_code=404, detail="movie not found.")
    
    # checking that the characters exist and are part of the movie
    if db.characters[conversation.character_1_id].movie_id != movie_id and  db.characters[conversation.character_2_id].movie_id != movie_id:
        raise HTTPException(status_code=400, detail="characters not in movie.")
    
    # checking that the characters are not the same
    if conversation.character_1_id == conversation.character_2_id:
        raise HTTPException(status_code=400, detail="characters are the same.")
    
    # checking that the lines match the characters
    for line in conversation.lines:
        if line.character_id != conversation.character_1_id and line.character_id != conversation.character_2_id:
            raise HTTPException(status_code=400, detail="line character id does not match given characters.")

    # create the conversation
    db.conversationId += 1
    newConvo = db.conversation(db.conversationId, conversation.character_1_id, conversation.character_2_id, movie_id)
    print("im here im here im here")
    # creating the lines
    for sort, l in enumerate(conversation.lines):
        db.lineId += 1
        newLine = db.line(db.lineId, l.character_id, movie_id, newConvo.conversation_id, sort, l.line_text)
        db.lines[newLine.line_id] = newLine
        db.characters[newLine.character_id].lines += 1

        # udpating newConvo attributes
        if newLine.character_id == newConvo.character1_id:
            newConvo.character1_lines += 1
        else:
            newConvo.character2_lines += 1
        newConvo.lineCount += 1

    # adding to conversations dictionary
    db.conversations[newConvo.conversation_id] = newConvo

    # updating lines file
    db.upload_new_lines()

    # updating conversations file
    db.upload_new_conversations()

    # db.logs.append({"post_call_time": datetime.now(), "movie_id_added_to": movie_id})
    # db.upload_new_log()

    # rerturns conversation id
    return newConvo.conversation_id
