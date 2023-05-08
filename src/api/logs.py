import datetime
from fastapi import APIRouter, HTTPException
from enum import Enum

from pydantic import BaseModel
from src import database as db
from sqlalchemy import *
from fastapi.params import Query

router = APIRouter()

class logJSON(BaseModel):
    user_id: int
    log_id: int
    current_lbs: int
    time_posted: datetime

@router.get("/logs/{user_id}", tags=["logs"])
def get_logs(user_id: int):
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

@router.post("/logs/{user_id}", tags=["logs"])
def create_log(log: logJSON):
    """
	'User_id': the id of the user who’s log this is being added to,
	'Log_id': the log that the workout is being added to,
	'Current_lbs': the weight of the user for the log,
	'Time_posted': datetime for the log
    """