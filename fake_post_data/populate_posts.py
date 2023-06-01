import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)


num_users = 200000
fake = Faker()

# create fake postes with fake names and birthdays
with engine.begin() as conn:
    print('creating fake users')
    logs = []
    for i in range(num_users):

        # every ten user it prints
        if (i % 10 == 0):
            print(i)

        