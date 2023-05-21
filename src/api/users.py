from fastapi import APIRouter, HTTPException
from sqlalchemy import *
from pydantic import BaseModel
import enum
from datetime import date
from src import database as db
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

router = APIRouter()


class GenderEnum(str, enum.Enum):
    M = "M"
    F = "F"


class UserJson(BaseModel):
    name: str
    starting_lbs: int
    height_inches: int
    avg_calorie_intake: int
    birthday: date
    gender: GenderEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    starting_lbs = Column(Integer, nullable=True)
    name = Column(Text, nullable=True)
    height_inches = Column(Integer, nullable=True)
    avg_calorie_intake = Column(Integer, nullable=True)
    birthday = Column(Date, nullable=True)
    gender = Column(Text, nullable=True)


@router.post("/users/", tags=["users"])
def create_user(user: UserJson):
    """
    This endpoints adds a user to the user databse. The user is represetned by a UserJson
    object which holds all the attributes for the user.

    Limitations:
    1. User must use Americans units for height and weight.
    2. Two users with the same name can be created, which will cause confusion for v2
    3. Birthday string must be in format YYYY-MM-DD
    """
    with db.engine.begin() as conn:

        # make sure that the height and weight is not negative

        if user.starting_lbs < 0:
            raise HTTPException(status_code=400, detail="Invalid weight")
        if int(user.height_inches) < 0:
            raise HTTPException(status_code=400, detail="Invalid height")
        birthday = user.birthday
        # newId = conn.execute(
        #     text("SELECT MAX(user_id) FROM users")).scalar_one()
        # newId = conn.execute(
        #     text("SELECT MAX(user_id) FROM users")).scalar_one()
        newUser = conn.execute(db.users.insert().values(starting_lbs=user.starting_lbs,
                                                  name=user.name,
                                                  height_inches=user.height_inches,
                                                  avg_calorie_intake=user.avg_calorie_intake,
                                                  birthday=birthday,
                                                  gender=user.gender))
        print(newUser.inserted_primary_key)
        return {"message": "user created successfully with id: " + str(newUser.inserted_primary_key[0]) + "."}


@router.get("/users/{id}", tags=["users"])
def get_user(id: int):
    """
    This endpoint returns a user's information based on their id. For each user it returns:
        * `user_id`: the internal id of the user.
        * `name`: The name of the user.
        * `starting_lbs`: The starting weight of the user.
        * `height_inches`: The height of the user.
        * `avg_calorie_intake`: The average calorie intake of the user.
        * 'birthday': The birthday of the user.
        * 'gender': the gender of the user.
    """
    json = None

    with db.engine.connect() as conn:
        user = conn.execute(
            text("SELECT * FROM users WHERE user_id = :id"), {"id": id}).fetchone()
        if user:
            json = {
                'user_id': user.user_id,
                'name': user.name,
                'starting_lbs': user.starting_lbs,
                'height_inches': user.height_inches,
                'avg_calorie_intake': user.avg_calorie_intake,
                'birthday': user.birthday,
                'gender': user.gender
            }

    if json is None:
        raise HTTPException(status_code=404, detail="user not found.")

    return json
