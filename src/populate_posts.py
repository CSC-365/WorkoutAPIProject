from sqlalchemy import *
import os
import dotenv
from faker import Faker
import numpy as np
import database as db
from api import business_logic as bl

import hashlib


num_users = 5
fake = Faker()
new_users = []

# create fake postes with fake names and birthdays


with db.engine.begin() as conn:
    for i in range(num_users):
        

        new_logs = []
        

        profile = fake.profile()
        weight = fake.random_int(min=0, max=350)        # could be changed later to test negative values and such
        height = fake.random_int(min=36, max=96)       # at least 3 feet tall, max 8 feet tall
        avg_calories = fake.random_int(min=1000, max=5000)  # at least 1000 calories, max 5000 calories
        birthday = profile['birthdate']
        gender = fake.random_element(elements=('M', 'F'))

        password = fake.password(length=10, special_chars=True, digits=True)
        salt = os.urandom(32)  # A new salt for this user
        key = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), salt, 100000)

        # insert a new user
        new_user = conn.execute(db.users.insert().values(starting_lbs=weight,
                                                        name=fake.name(),
                                                        height_inches=height,
                                                        avg_calorie_intake=avg_calories,
                                                        birthday=birthday,
                                                        gender=gender,
                                                        password=key,
                                                        salt=salt))
        
        user_id = new_user.inserted_primary_key[0]
        new_users.append(user_id)


        # create a goal for each user 
        goal_user = conn.execute(text("SELECT id, user, birthday, starting_lbs, height_inches, gender FROM users WHERE id = :id"), {"id": user_id}).fetchone()

        # generate a target weight <= 100 lbs less than the starting weight
        goal_weight = fake.random_int(min=weight-100, max=weight)
        try: 
                goal_distance, goal_times_per_week = bl.calculate_workout_plan(goal_user, goal_weight)
        except ValueError as ve:
            print(str(ve))
            continue

        new_workout = conn.execute(db.workouts.insert().values(
            workout_name="Run",
            weight=0,
            distance_ft=goal_distance,
            repetitions=None,
            seconds=None,
            sets=None,
            times_per_week=goal_times_per_week,
            user_id=user_id     # this id technically should match the user_id
        ))

        new_goal = conn.execute(db.goals.insert().values(
            type_id=0,
            user_id=user_id,
            target_weight=goal_weight,
            workout_id=new_workout.inserted_primary_key[0]
        )) 


        # create fake logs for each user 
        num_logs = fake.random_int(min=1, max=100)
        for j in range(num_logs):
            new_logs.append({
                # user_id is the id of the user that the log is being added to
                "user_id": user_id,

                # give me a random date between now and 5 years from now
                "time_posted": fake.date_time_between(start_date='now', end_date='+5y', tzinfo=None),

                # random weight between +/- 20 of what the generated weight is
                "current_lbs": fake.random_int(min=weight-20, max=weight+20)
            
            
            })
        
        # execute the log insert
        new_log = conn.execute(db.logs.insert().values(new_logs))
        log_id = new_log.inserted_primary_key[0]       

        if (i % 10 == 0):
            print("user number: " + str(i))
            print("id: " + str(user_id))


# new engine connection in order to commit new logs
with db.engine.begin() as conn:
    for user_id in new_users:

        # create 1-10 projections for each user
        num_projections= fake.random_int(min=1, max=10)
        new_projections = []

        # get the most recent log for the user 
        for k in range(num_projections):
            # ensure that the projection date is in the future & after the last log date
            projection_logs = conn.execute(
            text("SELECT current_lbs, time_posted FROM logs WHERE user_id = :user_id ORDER BY time_posted"),
            {"user_id": user_id}).fetchall()

            projection_date = fake.date_between(start_date='now', end_date='+5y')
            last_log_date = projection_logs[-1].time_posted.date()
            while (projection_date < last_log_date):
                projection_date = fake.date_between(start_date='now', end_date='+5y')

            # calculate the projection

            try:
                projected_loss = bl.calculate_projection(
                    projection_logs, projection_date)
            except ValueError as ve:
                print(str(ve))
                continue
        
            # add to the new projection list
            new_projections.append({
                "user_id": user_id,
                "projection_lbs": projected_loss,
                "projection_date": projection_date,
                "date_posted": last_log_date # date posted is last log date 
            })

        # execute the projection insert
        new_projection = conn.execute(db.projection.insert().values(new_projections))


