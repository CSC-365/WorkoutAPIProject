from fastapi import FastAPI
from src.api import users, pkg_util, goals, logs, workouts, projection

description = """
Workout API returns workout information based on a user's physical attributes and goals. 

## Users

You can:
* **Create a user based on personal information**
* **Retrieve a user's information based on their id**
* **Login as user with your name and password**

## Goals

You can:
* **Create a goal based on a user's id and goal information**

## Logs
You can:
* **Create a log based on a user's id and log information**
* **Retrieve logs for a given user**

## Workouts
You can:
* **Retrieve workouts for a given user id**

## Projections
You can:
* **Retrieve a user's projections**
* **Create a new projection for a user**

"""
tags_metadata = [
    {
        "name": "users",
        "description": "Access information on users in the Workout API.",
    },
    {
        "name": "goals",
        "description": "Access information on goals in the Workout API.",
    },
    {
        "name": "logs",
        "description": "Access information on logs in the Workout API.",
    },
    {
        "name": "workouts",
        "description": "Access information on workouts in the Workout API.",
    },
    {
        "name": "projection",
        "description": "Access information on projections in the Workout API.",
    },
]

app = FastAPI(
    title="Workout API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Kenneth Choi",
        "email": "kchoi21@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(users.router)
app.include_router(goals.router)
app.include_router(pkg_util.router)
app.include_router(logs.router)
app.include_router(workouts.router)
app.include_router(projection.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Workout API. See /docs for more information."}
