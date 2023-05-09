import datetime
from fastapi import APIRouter, HTTPException
from enum import Enum

from pydantic import BaseModel
from sqlalchemy.sql.functions import current_timestamp

from src import database as db
from sqlalchemy import *
from fastapi.params import Query

router = APIRouter()


class logJSON(BaseModel):
    user_id: int
    # log_id: int               log will be created when the log posts
    current_lbs: int
    # time_posted: datetime causes an error + it will be created when the log is created


@router.get("/logs/{user_id}", tags=["logs"])
def get_logs(id: int):
    """
    This endpoint returns all the logs in the database for a given user. For each log it returns:
    'User_id': user_id,
	'Name': name of the user,
	'Logs': list of logs
	
    Each log is represented by a dictionary with the following keys:
        'Log_id': id of the log,
        'Current_lbs':	weight associated with the log,
        'Time_posted': time the log was posted
    
    """
    meta = MetaData()
    json = None
    logJSON = None
    with db.engine.connect() as conn:
        user = conn.execute(text("SELECT * FROM users WHERE user_id =:id"), {"id": id}).fetchone()
        logs = conn.execute(text("SELECT * FROM log WHERE user_id=:id"), {"id": id}).fetchall()
        if user:
            json = {
                "user_id": user.user_id,
                "name": user.name,
                "logs": [{
                    "log_id": log.log_id,
                    "current_lbs" : log.current_lbs,
                    "time_posted" : log.time_posted
                } for log in logs]
            }
    if json is None:
        raise HTTPException(status_code=404, detail="user not found")
    return json





"""
Input Structure:
{
    "User_id": 
    "Log_id":
    "Current_lbs":
    "Time_posted": datetime for the log
}
"""


@router.post("/logs/", tags=["logs"])
def create_log(log: logJSON):
    """
	'User_id': the id of the user who’s log this is being added to,
	'Log_id': the log that the workout is being added to,
	'Current_lbs': the weight of the user for the log,
	'Time_posted': datetime for the log
    """

    meta = MetaData()
    logs = Table('log', meta, autoload_with=db.engine)
    users = Table('users', meta, autoload_with=db.engine)
    workouts = Table('workouts', meta, autoload_with=db.engine)

    with db.engine.begin() as conn:
        newLogId = conn.execute(text("SELECT MAX(log_id) FROM log")).fetchone()[0]
        newLog = conn.execute(logs.insert().values(user_id=log.user_id,
                                                   log_id=0 if newLogId is None else newLogId + 1,
                                                   current_lbs=log.current_lbs,
                                                   time_posted=current_timestamp()))
        return {"Message": "Log successfully created with id: " + str(newLogId)}
