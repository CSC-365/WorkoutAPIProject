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


@router.post("/logs/{id}", tags=["logs"])
def create_log(user: logJSON):
    """
    This endpoint adds a workout to the users workout log database

    Limitations:
    1. User must use pounds for weight
    """
    meta = MetaData()
    logs = Table('logs', meta, autoload_with=db.engine)
    with db.engine.begin() as conn:

    