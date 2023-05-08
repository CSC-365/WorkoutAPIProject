from fastapi import APIRouter, HTTPException
from enum import Enum

from pydantic import BaseModel
from src import database as db
from sqlalchemy import *
from fastapi.params import Query

router = APIRouter()
class GoalJson(BaseModel):
    type_id: int            # removed user & goal id in order to get the id's from the database rather
    target_weight: int
    workout_id: int

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


       # create the goal


       if goal.type_id == 0:   # weight type --> run
           conn.execute(goals.insert().values(goal_id = 0 if newGoalId is None else newGoalId + 1, type_id = goal.type_id, user_id = goal.user_id, target_weight = goal.target_weight, workout_id = newWorkoutId))
           user = conn.execute(text("SELECT * FROM users WHERE user_id = :id"), {"id": goal.user_id}).fetchone()
      
           # Calculate basal metabolic rate using the Harris-Benedict equation
           bmr = 88.362 + (13.397 * user.starting_lbs) + (4.799 * user.height_inches) - (5.677 * user.age)


           # Adjust basal metabolic rate based on activity level
           if user.avg_calorie_intake < bmr:
               bmr *= 1.2
           elif user.avg_calorie_intake > bmr:
               bmr *= 1.5


           # Calculate the calorie deficit needed to reach the target weight
           calorie_deficit = (user.starting_lbs - goal.target_weight) * 3500


           # Calculate the daily running distance needed to achieve the calorie deficit
           distance_ft = calorie_deficit / 100


           # user is going to run 7x per week for v1
           conn.execute(workouts.insert().values(workout_id = 0 if newWorkoutId is None else newWorkoutId, workout_name = "Run", weight = 0, distance_ft = distance_ft, repetitions = None, seconds = None, sets = None,  times_per_week = 7))
   return {"message": "Goal created successfully with id: " + str(newGoalId) + " and workout id: " + str(newWorkoutId)}      

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