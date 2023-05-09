from fastapi import APIRouter, HTTPException
from enum import Enum

from pydantic import BaseModel
from src import database as db
from sqlalchemy import *
from fastapi.params import Query

router = APIRouter()
class GoalJson(BaseModel):
    user_id: int
    type_id: int            
    target_weight: int

@router.post("/goals/", tags=["goals"])
def create_goal(goal: GoalJson):
    """
    This endpoint adds a goal to the goals database. The goals are represented by a GoalJson.
    Upon creation of a goal, the user will be assigned a workout plan based on the associated information.
    That is then added to the workout database.
    """
    meta = MetaData()
    goals = Table('goals', meta, autoload_with = db.engine)
    workouts = Table('workouts', meta, autoload_with = db.engine)
    users = Table('users', meta, autoload_with = db.engine)


    with db.engine.begin() as conn:


        # make sure that the type_id is in the range of acceptable plans
        # right now its just 0
        if goal.type_id != 0:
           raise HTTPException(status_code=400, detail="Invalid type_id")
      
        newGoalId = conn.execute(text("SELECT MAX(goal_id) FROM goals")).fetchone()[0]
        newWorkoutId = conn.execute(text("SELECT MAX(workout_id) FROM workouts")).fetchone()[0]
        
        if goal.type_id == 0:   # weight type --> run
            conn.execute(goals.insert().values(goal_id = 0 if newGoalId is None else newGoalId + 1, type_id = goal.type_id, user_id = goal.user_id, target_weight = goal.target_weight, workout_id = newWorkoutId))
            user = conn.execute(text("SELECT * FROM users WHERE user_id = :id"), {"id": goal.user_id}).fetchone()
      

            # Calculate basal metabolic rate (BMR)
            bmr = 10 * user.starting_lbs + 6.25 * user.height_inches - 5 * user.age + 5 if user.gender == 'M' else 10 * user.starting_lbs + 6.25 * user.height_inches - 5 * user.age - 161

            # Calculate total daily energy expenditure (TDEE)
            tdee = bmr * 1.55

            # Calculate daily caloric deficit
            daily_caloric_deficit = 500 * (user.starting_lbs - goal.target_weight)

            # Calculate feet per week needed to lose weight
            miles_per_week = daily_caloric_deficit / 100
            feet_per_week = miles_per_week * 5280

            # user is going to run 7x per week for v1
            conn.execute(workouts.insert().values(workout_id = 0 if newWorkoutId is None else newWorkoutId + 1, workout_name = "Run", weight = 0, 
                                                  distance_ft = feet_per_week / 7, repetitions = None, seconds = None, sets = None,  
                                                  times_per_week = 7, user_id = goal.user_id))
    return {"message": "Goal created successfully with id: " + str(newGoalId + 1) + " and workout id: " + str(newWorkoutId + 1)}      

