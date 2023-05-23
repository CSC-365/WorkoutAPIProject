from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.sql.functions import current_timestamp
from src import database as db
from datetime import date
from sqlalchemy import *

router = APIRouter()

class projectionJSON(BaseModel):
    projection_date: date


@router.post("/user/{user_id}/projection", tags=["projection"])
def create_projection(user_id: int, projection: projectionJSON):
    """
    This endpoint craetes the projections for the user based on the user's previous logs
    and its target date. 
    """

    with db.engine.begin() as conn:
        # get me all the logs based on the given user id
        logs = conn.execute(
            text("SELECT current_lbs, time_posted FROM log WHERE user_id = :user_id ORDER BY time_posted"), {"user_id": user_id}).fetchall()
        
        if len(logs) == 0: # meaning they have no logs
            raise HTTPException(status_code=404, detail="user has no logs")
        # write me a similar query getting the user
        # user = conn.execute(
        #     text("SELECT * FROM users WHERE id = :id"), {"id": user_id}).fetchone()

        # x-axis difference in days
        x = (logs[-1].time_posted.date() - logs[0].time_posted.date()).days

        # y-axis difference in lbs
        y = logs[-1].current_lbs - logs[0].current_lbs

        # slope
        m = round(y / x, 2)

        days = (projection.projection_date - date.today()).days
        projectedLoss = int(round(logs[-1].current_lbs + (days * m), 0))

        newP = conn.execute(db.projection.insert().values(user_id=user_id,
                                                            projection_lbs=projectedLoss,
                                                            projection_date=projection.projection_date,
                                                            date_posted=current_timestamp()))
    
        return {"Message": "Projection successfully created with id: " + str(newP.inserted_primary_key[0]) + "."}
    
@router.get("/user/{user_id}/projection", tags=["projection"])
def get_projection(user_id: int = Query(ge=0)):
    """
    This endpoint returns all the projections in the database for a given user. For each projection it returns:
    * 'User_id': user_id,
    * 'Name': name of the user,
    * 'Projections': list of projections

    Each projection is represented by a dictionary with the following keys:
    * 'Projection_id': id of the projection
    * 'Projection_lbs':	weight associated with the projection
    * 'Projection_date': date for the projection
    * 'Date_posted': date the projection was posted
    """
    json = None
    with db.engine.connect() as conn:
        # this needs to be changed to using sqlalchemy
        """if user_id < 0:
            raise HTTPException(
                status_code=400, detail="id cannot be negative")"""
        user = conn.execute(
            text("SELECT id, name FROM users WHERE id =:user_id"), {"user_id": user_id}).fetchone()
        projections = conn.execute(
            text("SELECT projection_id, projection_lbs, projection_date, date_posted FROM projection WHERE user_id=:user_id ORDER BY date_posted"), {"user_id": user_id}).fetchall()
        
        if user:
            json = {
                "user_id": user.id,
                "name": user.name,
                "projections": [{
                    "projection_id": projection.projection_id,
                    "projection_lbs": projection.projection_lbs,
                    "projection_date": projection.projection_date,
                    "date_posted": projection.date_posted
                } for projection in projections]
            }
    if json is None:
        raise HTTPException(status_code=404, detail="user not found")
    return json