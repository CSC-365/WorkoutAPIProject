import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db
from sqlalchemy import *
router = APIRouter()


class GoalJson(BaseModel):
    user_id: int
    type_id: int
    target_weight: int


@router.post("/goals/", tags=["goals"])
def create_goal(goal: GoalJson):
    """
    This endpoint adds a goal to the goals database. The goals are represented by a GoalJson.
    Upon creation of a goal, a workout will be created based on the associated information.
    That is then added to the workout database.
    """
    with db.engine.begin() as conn:
        # make sure that the type_id is in the range of acceptable plans
        # right now its just 0
        if goal.type_id != 0:
            raise HTTPException(status_code=400, detail="Invalid type_id")

        user = conn.execute(
            text("SELECT * FROM users WHERE id = :id"), {"id": goal.user_id}).fetchone()

        # Calculate basal metabolic rate (BMR)
        current_date = datetime.date.today()
        age = current_date.year - user.birthday.year
        bmr = 10 * user.starting_lbs + 6.25 * user.height_inches - 5 * age + \
            5 if user.gender == 'M' else 10 * user.starting_lbs + \
            6.25 * user.height_inches - 5 * age - 161

        # Calculate total daily energy expenditure (TDEE)
        tdee = bmr * 1.55

        # Calculate daily caloric deficit
        daily_caloric_deficit = 500 * (user.starting_lbs - goal.target_weight)

        # Calculate feet per week needed to lose weight
        miles_per_week = daily_caloric_deficit / 100
        feet_per_week = miles_per_week * 5280

        # user is going to run 7x per week for v1
        newWorkout = conn.execute(db.workouts.insert().values(workout_name="Run", weight=0,
                                                 distance_ft=feet_per_week / 7,
                                                 repetitions=None,
                                                 seconds=None,
                                                 sets=None,
                                                 times_per_week=7,
                                                 user_id=goal.user_id))
        # need to get the workout id
        workout_id = newWorkout.inserted_primary_key[0]
        conn.execute(db.goals.insert().values(type_id=goal.type_id,
                                              user_id=goal.user_id,
                                              target_weight=goal.target_weight,
                                              workout_id=workout_id))
    return {"message": "Goal created successfully."}
