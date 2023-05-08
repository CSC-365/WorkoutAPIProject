from fastapi import FastAPI
from src.api import users, pkg_util

description = """
Workout API returns workout information based on a user's physical attributes and goals.

## Users

You can:
* **Create a user based on personal information**
* **Retrieve a user's information based on their id**

"""
tags_metadata = [
    {
        "name": "users",
        "description": "Access information on users in the Workout API.",
    }
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
app.include_router(pkg_util.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Workout API. See /docs for more information."}
