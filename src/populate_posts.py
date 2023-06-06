from sqlalchemy import *
import os
import dotenv
from faker import Faker
import numpy as np
import database as db
from api import business_logic as bl

import hashlib

# get the first user id for incrementing

num_users = 200000
fake = Faker()
new_users = []  # used for id's but now used for user objects
new_workouts = []  # list of workouts, index will relate to the user
new_goals = []  # list of goals, index will relate to the user
new_logs = []  # list of logs, index will relate to the user
new_projections = []  # list of projections, index will relate to the user

inserted_users = [] # list of inserted users
goal_weights = [] # list of goal weights, index will relate to the user


# create fake postes with fake names and birthdays


with db.engine.begin() as conn:
    for i in range(num_users):
        if i % 1000 == 0:
            print(f"Creating user {i}")
        # get the greatest current id

        profile = fake.profile()
        weight = fake.random_int(min=0, max=350)        # could be changed later to test negative values and such
        height = fake.random_int(min=36, max=96)    
        avg_calories = fake.random_int(min=1000, max=5000)  # at least 1000 calories, max 5000 calories
        birthday = profile["birthdate"]
        gender = fake.random_element(elements=('M', 'F'))
        new_users.append({
            "name": fake.name(),
            "starting_lbs": weight,
            "height_inches": height,
            "avg_calorie_intake": avg_calories,
            "birthday": birthday,
            "gender": gender,
            "password": None,
            "salt": None
        })

    inserted_users = conn.execute(db.users.insert().values(new_users).returning(db.users)).fetchall()


# for each user, create a its logs and then workout (adding the goal weight for later)
with db.engine.begin() as conn:
    for user in inserted_users:
        num_logs = fake.random_int(min=3, max=5)
        log_dates = set()
        for j in range(num_logs):
            log_date = fake.date_time_between(start_date='now', end_date='+5y', tzinfo=None)
            while log_date in log_dates:
                log_date = fake.date_time_between(start_date='now', end_date='+5y', tzinfo=None)
            log_dates.add(log_date)
            new_logs.append({
                # user_id is the id of the user that the log is being added to
                "user_id": user.id,
                # give me a random date between now and 5 years from now
                "time_posted": log_date,

                # random weight between +/- 20 of what the generated weight is
                "current_lbs": fake.random_int(min=weight-20, max=weight+20)
    })
        
        # generate a target weight <= 100 lbs less than the starting weight
        goal_weight = fake.random_int(min=user.starting_lbs-100, max=user.starting_lbs)

        # add goal weight for goals later
        goal_weights.append(goal_weight)
        try: 
                goal_distance, goal_times_per_week = bl.calculate_workout_plan(user, goal_weight)
        except ValueError as ve:
            print(str(ve))
            continue

        new_workouts.append({
            "user_id": user.id,
            "workout_name": "Run",
            "weight": 0,
            "distance_ft": goal_distance,
            "repetitions": None,
            "seconds": None,
            "sets": None,
            "times_per_week": goal_times_per_week,
        })
    new_workouts = conn.execute(db.workouts.insert().values(new_workouts).returning(db.workouts)).fetchall()



with db.engine.begin() as conn:
    for i, w in enumerate(new_workouts):
        if i % 1000 == 0:
            print(f"Creating goal {i}")
        # create a new goal for the associated workout
        new_goals.append({
            "user_id": w.user_id, # this id technically should match the user_id
            "workout_id": w.id,
            "type_id": 0,
            "target_weight": goal_weights[i],
        })

    # execute logs & goal inserts
    new_logs = conn.execute(db.logs.insert().values(new_logs).returning(db.logs)).fetchall()
    conn.execute(db.goals.insert().values(new_goals))


# new engine connection in order to commit new logs

with db.engine.begin() as conn:
    j = 0
    for i, user in enumerate(inserted_users):
        if i % 1000 == 0:
            print(f"creating projections for user {user.id}")
        # create 1-10 projections for each user
        num_projections= fake.random_int(min=1, max=3)
        
        projection_logs = []
        while(j < len(new_logs) and new_logs[j].user_id == user.id):
            projection_logs.append(new_logs[j])
            j += 1

        # get the most recent log for the user 
        for k in range(num_projections):
            print("creating projection " + str(k)) 
            # ensure that the projection date is in the future & after the last log date
            # projection_logs = conn.execute(
            # text("SELECT current_lbs, time_posted FROM logs WHERE user_id = :user_id ORDER BY time_posted"),
            # {"user_id": user.id}).fetchall()

            projection_date = fake.date_between(start_date=projection_logs[-1].time_posted.date(), end_date='+5y')

            # calculate the projection

            try:
                projected_loss = bl.calculate_projection(
                    projection_logs, projection_date)
            except ValueError as ve:
                print(str(ve))
                continue
        
            # add to the new projection list
            new_projections.append({
                "user_id": user.id,
                "projection_lbs": projected_loss,
                "projection_date": projection_date,
                "date_posted": projection_logs[-1].time_posted.date() # date posted is last log date 
            })

    # execute the projection inserts
    conn.execute(db.projection.insert().values(new_projections))
