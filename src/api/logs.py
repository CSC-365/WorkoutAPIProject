from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.sql.functions import current_timestamp
from src import database as db
from sqlalchemy import *

router = APIRouter()


class logJSON(BaseModel):
    current_lbs: int


@router.get("/user/{user_id}/logs", tags=["logs"])
def get_logs(user_id: int = Query(ge=0)):
    """
    This endpoint returns all the logs in the database for a given user. For each log it returns:
    * 'User_id': user_id,
    * 'Name': name of the user,
    * 'Logs': list of logs

    Each log is represented by a dictionary with the following keys:
    * 'Log_id': id of the log,
    * 'Current_lbs':	weight associated with the log,
    * 'Time_posted': time the log was posted
    """
    json = None
    with db.engine.connect() as conn:
        user = conn.execute(
            text("SELECT id, name FROM users WHERE id =:user_id"), {"user_id": user_id}).fetchone()
        logs = conn.execute(
            text(
                "SELECT id, current_lbs, time_posted FROM logs WHERE user_id=:user_id"),
            {"user_id": user_id}).fetchall()
        if user:
            json = {
                "user_id": user.id,
                "name": user.name,
                "logs": [{
                    "log_id": log.id,
                    "current_lbs": log.current_lbs,
                    "time_posted": log.time_posted
                } for log in logs]
            }
    if json is None:
        raise HTTPException(status_code=404, detail="user not found")
    return json


@router.post("/user/{user_id}/logs", tags=["logs"])
def create_log(user_id: int, log: logJSON):
    """
    This endpoint creates a new log for a given user

    Each log contains the following keys:
    * 'Log_id': the log that the workout is being added to,
    * 'User_id': the id of the user who’s log this is being added to,
    * 'Current_lbs': the weight of the user for the log,
    * 'Time_posted': datetime for the log
    """

    with db.engine.begin() as conn:
        # if user_id < 0:
        #     raise HTTPException(status_code=400, detail="invalid user Id")
        userCheck = conn.execute(
            text("SELECT id FROM users WHERE id = :user_id"), {"user_id": user_id}).fetchone()
        if userCheck is None:
            raise HTTPException(status_code=404, detail="user not found")

        if log.current_lbs < 0:
            raise HTTPException(status_code=400, detail="invalid weight")

        result = conn.execute(db.logs.insert().values(user_id=user_id,
                                                      current_lbs=log.current_lbs,
                                                      time_posted=current_timestamp()).returning(db.logs.c.id))
        newLogId = result.fetchone()[0]

        return {newLogId}
