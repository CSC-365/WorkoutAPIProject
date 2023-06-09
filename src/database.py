from sqlalchemy import *
import os
import dotenv
import sqlalchemy


# conenction via the supabase url
def database_connection_url():

    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


# creating a new DB engine based on our connection string
engine = sqlalchemy.create_engine(
    database_connection_url(), echo=True, future=True)


meta = MetaData()
workouts = Table('workouts', meta, autoload_with=engine)
users = Table('users', meta, autoload_with=engine)
logs = Table('logs', meta, autoload_with=engine)
goals = Table('goals', meta, autoload_with=engine)
projection = Table('projection', meta, autoload_with=engine)

sorted_tables = [users, workouts, logs, goals, projection]
tables = {"users": users, "workouts": workouts,
          "logs": logs, "goals": goals, "projection": projection}
