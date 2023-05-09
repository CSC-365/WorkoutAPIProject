from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import *
from pydantic import BaseModel

from src import database as db

router = APIRouter()

@router.get("/workouts/{user_id}", tags=["workouts"])
def get_workouts(user_id: int):
    """
    This endpoint returns a user's workout information based on their id. For each user it returns:
    * 'User_id': user_id
	* 'Workouts': a list of workouts

    each workout consists of:
        * 'Workout_id': workout_ id
        * 'workout_name': name of the workout,
        * 'Weight': the weight for the workout, null if not applicable
        * 'Distance_ft': the distance for the workout
        * 'Repetitions': number of repetiontions for the workout
        * 'Seconds': duration of the workout in seconds, null if not applicable
        * 'Sets': number of sets of the workout
        * 'Times_per_week': the number of times per week the workout is performed
    """
    meta = MetaData()
    workouts = Table('workouts', meta, autoload_with = db.engine)
    users = Table('users', meta, autoload_with = db.engine)

    with db.engine.begin() as conn:
        user = conn.execute(text("SELECT * FROM users WHERE user_id = :id"), {"id": user_id}).fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        workouts = conn.execute(text("SELECT * FROM workouts WHERE user_id = :id"), {"id": user_id}).fetchall()
        workout_list = []
        for workout in workouts:
            workout_list.append({
                'Workout_id': workout.workout_id,
                'Workout_name': workout.workout_name,
                'Weight': workout.weight,
                'Distance_ft': workout.distance_ft,
                'Repetitions': workout.repetitions,
                'Seconds': workout.seconds,
                'Sets': workout.sets,
                'Times_per_week': workout.times_per_week
            })
        return {'User_id': user_id, 'Workouts': workout_list}
    


