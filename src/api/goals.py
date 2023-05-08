from fastapi import APIRouter, HTTPException
from enum import Enum

from pydantic import BaseModel
from src import database as db
from sqlalchemy import *
from fastapi.params import Query

router = APIRouter()
class goalJSON(BaseModel):
    user_id: int
    type_id: int
    goal_id: int
    target_weight: int
    workout_id: int

@router.get("/goals/{id}", tags=["goals"])
def get_goals(goal_id: int):
    """
    This endpoint returns all the goals in the database. For each goal it returns:
    * 'User_id': user_id,
	* 'User_name': name of the user
	* 'Goals': list of the user’s goals 

    Each goal is represented by a dictionary with the following keys:
    * `goal_id`: the internal id of the goal.
    * 'type': The type of the goal.
    * 'target_weight': The target weight of the goal.
    """

@router.post("/goals/{id}", tags=["goals"])
def create_goal(goal_id: int):
    """
    This endpoint adds a goal to the goal database. The goal is represented by a GoalJson

	* 'user_id': the user id of the goal, 
	* 'Type_id': the type of workout (linked to a goal_type table)
	* 'goal_id': the id of the goal, 
	* 'Target_weight': the target weight for the goal
    * 'Workout_id': id of the workout that is produced from the goal
    """