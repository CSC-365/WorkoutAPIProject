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

if supabase_api_key is None or supabase_url is None:
    raise Exception(
        "You must set the SUPABASE_API_KEY and SUPABASE_URL environment variables."
    )


# # THIS CODE IS ALL FOR READING FROM CSVS DELETE DELETE DELETE

# supabase: Client = create_client(supabase_url, supabase_api_key)
# sess = supabase.auth.get_session()

# # Reading in the log file from the supabase bucket
# log_csv = (
#     supabase.storage.from_("movie-api")
#     .download("movie_conversations_log.csv")
#     .decode("utf-8")
# )

# logs = []
# for row in csv.DictReader(io.StringIO(log_csv), skipinitialspace=True):
#     logs.append(row)


# # Writing to the log file and uploading to the supabase bucket
# def upload_new_log():
#     output = io.StringIO()
#     csv_writer = csv.DictWriter(
#         output, fieldnames=["post_call_time", "movie_id_added_to"]
#     )
#     csv_writer.writeheader()
#     csv_writer.writerows(logs)
#     supabase.storage.from_("movie-api").upload(
#         "movie_conversations_log.csv",
#         bytes(output.getvalue(), "utf-8"),
#         {"x-upsert": "true"},
#     )

# # Writing to the lines file and uploading to the supabase bucket

# def upload_new_lines():
#     output = io.StringIO()
#     csv_writer = csv.DictWriter(
#         output, fieldnames=["line_id", "character_id", "movie_id", "conversation_id", "line_sort", "line_text"]
#     )
#     csv_writer.writeheader()
#     linesList = []
#     for cur in lines.values():
#         cur = vars(cur)
#         linesList.append(cur)
#     linesList = sorted(linesList, key=lambda x: x["line_id"])
#     csv_writer.writerows(linesList)
#     supabase.storage.from_("movie-api").upload(
#         "lines.csv",
#         bytes(output.getvalue(), "utf-8"),
#         {"x-upsert": "true"},
#     )

# # Writing to the conversations file and uploading to the supabase bucket

# def upload_new_conversations():
#     output = io.StringIO()
#     csv_writer = csv.DictWriter(
#         output, fieldnames=["conversation_id", "character1_id", "character2_id", "movie_id"]
#     )
#     csv_writer.writeheader()
#     conversationsList = []
#     for cur in conversations.values():
#         curConvo = {"conversation_id": cur.conversation_id, "character1_id": cur.character1_id, "character2_id": cur.character2_id, "movie_id": cur.movie_id}
#         conversationsList.append(curConvo)
#     conversationsList = sorted(conversationsList, key=lambda x: x["conversation_id"])
#     csv_writer.writerows(conversationsList)
#     supabase.storage.from_("movie-api").upload(
#         "conversations.csv",
#         bytes(output.getvalue(), "utf-8"),
#         {"x-upsert": "true"},
#     )


# def try_parse(type, val):
#     try:
#         return type(val)
#     except ValueError:
#         return None

# class movie:

#     def __init__(self, movie_id: int, title: str, year: int, imdb_rating: float, imdb_votes: int, raw_script_url: str):
#         self.movie_id  = movie_id
#         self.title = title
#         self.year = year
#         self.imdb_rating = imdb_rating
#         self.imdb_votes = imdb_votes
#         self.raw_script_url = raw_script_url

# class character:

#     def __init__(self, character_id: int, name: str, movie_id: int, gender: str, age: int):
#         self.character_id = character_id
#         self.name = (name or None)
#         self.movie_id = movie_id
#         self.gender = (gender or None)
#         self.age = age
#         self.lines = 0      # integer to count the amount of lines within the movie
    


# class conversation:

#     def __init__(self, conversation_id: int, character1_id: int, character2_id: int, movie_id: int):
#         self.conversation_id = conversation_id
#         self.character1_id = character1_id
#         self.character2_id = character2_id
#         self.movie_id = movie_id
#         self.lineCount = 0      # line count is initially zero to be added later
#         self.character1_lines = 0
#         self.character2_lines = 0

# class line:

#     def __init__(self, line_id: int, character_id: int, movie_id: int, conversation_id: int, line_sort: int, line_text: str):
#         self.line_id = line_id
#         self.character_id = character_id
#         self.movie_id = movie_id
#         self.conversation_id = conversation_id
#         self.line_sort = line_sort
#         self.line_text = line_text

# # different than (val or None) because if val = 0, it would return None
# def typeCheck(type, val):
#     try: 
#         return type(val)
#     except ValueError:
#         return None


# lines_csv = (
# supabase.storage.from_("movie-api")
# .download("lines.csv")
# .decode("utf-8")
# )

# lines = {}
# lineId = float("-inf") # negative infinity float used to add the lines to the end of the file everytime (allows for easier visuals)

# # -- local file traversal --
# # with open("lines.csv", mode="r", encoding="utf8") as csv_file:
# #     for row in csv.DictReader(csv_file, skipinitialspace=True):
# #         cur = line(typeCheck(int, row['line_id']), typeCheck(int,row['character_id']), typeCheck(int, row['movie_id']), typeCheck(int, row['conversation_id']), typeCheck(int, row['line_sort']), str(row['line_text']))
# #         lines[cur.line_id] = cur
# for row in csv.DictReader(io.StringIO(lines_csv), skipinitialspace=True):
#     cur = line(typeCheck(int, row['line_id']), typeCheck(int,row['character_id']), typeCheck(int, row['movie_id']), typeCheck(int, row['conversation_id']), typeCheck(int, row['line_sort']), str(row['line_text']))
#     lines[cur.line_id] = cur
#     lineId = max(lineId, cur.line_id)

# conversations_csv = (
# supabase.storage.from_("movie-api")
# .download("conversations.csv")
# .decode("utf-8")
# )

# conversations = {}
# conversationId = float("-inf") # negative infinity float used to add the conversations to the end of the file everytime (allows for easier visuals)
# # -- local file traversal --
# # with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
# #     for row in csv.DictReader(csv_file, skipinitialspace=True):
# #         cur = conversation(typeCheck(int, row['conversation_id']), typeCheck(int, row['character1_id']), typeCheck(int, row['character2_id']), typeCheck(int, row['movie_id']))
# #         conversations[cur.conversation_id] = cur

# for row in csv.DictReader(io.StringIO(conversations_csv), skipinitialspace=True):
#     cur = conversation(typeCheck(int, row['conversation_id']), typeCheck(int, row['character1_id']), typeCheck(int, row['character2_id']), typeCheck(int, row['movie_id']))
#     conversations[cur.conversation_id] = cur
#     conversationId = max(conversationId, cur.conversation_id)

# print(conversationId)
# movies = {}
# with open("movies.csv", mode="r", encoding="utf8") as csv_file:
#     for row in csv.DictReader(csv_file, skipinitialspace=True):
#         cur = movie(typeCheck(int, row['movie_id']), str(row['title']), str(row['year']), typeCheck(float, row['imdb_rating']), typeCheck(int, row['imdb_votes']), str(row['raw_script_url']))
#         movies[cur.movie_id] = cur

# characters = {}
# charNames = defaultdict(list)
# with open("characters.csv", mode="r", encoding="utf8") as csv_file:
#     for row in csv.DictReader(csv_file, skipinitialspace=True):
#         cur = character(typeCheck(int, row['character_id']), str(row['name']), typeCheck(int, row['movie_id']), str(row['gender']), typeCheck(int, row['age']))
#         characters[cur.character_id] = cur
#         charNames[cur.name].append(cur.character_id)

# # calculating line count 
# for l in lines.values():

#     # adding the conversation count
#     conversations[l.conversation_id].lineCount += 1
    
#     if l.character_id == conversations[l.conversation_id].character1_id:
#         conversations[l.conversation_id].character1_lines += 1
#     else:
#         conversations[l.conversation_id].character2_lines += 1

#     # adding the lines per character
#     characters[l.character_id].lines += 1
