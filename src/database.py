from collections import defaultdict
from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy
import csv  # csv reader
import io   # csv reader
from supabase import Client, create_client

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
engine = sqlalchemy.create_engine(database_connection_url(), echo=True, future=True)

supabase_api_key = os.environ.get("SUPABASE_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")

# if supabase_api_key is None or supabase_url is None:
#     raise Exception(
#         "You must set the SUPABASE_API_KEY and SUPABASE_URL environment variables."
#     )
