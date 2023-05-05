from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from sqlalchemy import *
from fastapi.params import Query

router = APIRouter()



@router.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: int):
    """
    This endpoint returns a single movie by its identifier. For each movie it returns:
    * `movie_id`: the internal id of the movie.
    * `title`: The title of the movie.
    * `top_characters`: A list of characters that are in the movie. The characters
      are ordered by the number of lines they have in the movie. The top five
      characters are listed.

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `num_lines`: The number of lines the character has in the movie.

    """

    json = None
    with db.engine.connect() as conn:
        movie = conn.execute(text("SELECT * FROM movies WHERE movie_id = :id"), {"id":movie_id}).fetchone()
        if movie:
            cs = conn.execute(text("SELECT c.*, COUNT(*) line_count FROM characters AS c JOIN lines AS l ON c.character_id = l.character_id WHERE c.movie_id = :id GROUP BY c.character_id ORDER BY line_count DESC"), {"id":movie_id}).fetchmany(5)
            topCs = []
            for c in cs:
                topCs.append({
                    "character_id": c.character_id,
                    "character": c.name,
                    "num_lines": c.line_count
                })
            
            json = {
                "movie_id": movie_id,
                "title": movie.title,
                "top_characters": topCs
            }

    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")
    return json        
    if movie_id in db.movies:
        chars = []
        
        for character in db.characters.values():
            if character.movie_id == movie_id:
                chars.append(character)
    
        chars = sorted(chars, key=lambda x: x.lines, reverse = True)
        chars = chars[:5]

        charsList = []
        for character in chars:
            curJson = {
                "character_id": character.character_id,
                "character": character.name,
                "num_lines": character.lines
            }
            charsList.append(curJson)
        json = {
            "movie_id": movie_id,
            "title": db.movies[movie_id].title,
            "top_characters": charsList
        }
    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return json

class movie_sort_options(str, Enum):
    movie_title = "movie_title"
    year = "year"
    rating = "rating"


# Add get parameters
@router.get("/movies/", tags=["movies"])
def list_movies(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: movie_sort_options = movie_sort_options.movie_title,
):
    """
    This endpoint returns a list of movies. For each movie it returns:
    * `movie_id`: the internal id of the movie. Can be used to query the
      `/movies/{movie_id}` endpoint.
    * `movie_title`: The title of the movie.
    * `year`: The year the movie was released.
    * `imdb_rating`: The IMDB rating of the movie.
    * `imdb_votes`: The number of IMDB votes for the movie.

    You can filter for movies whose titles contain a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `movie_title` - Sort by movie title alphabetically.
    * `year` - Sort by year of release, earliest to latest.
    * `rating` - Sort by rating, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    metadata = MetaData()
    movies = Table('movies', metadata, autoload_with=db.engine)
    if sort == movie_sort_options.movie_title:
        s = movies.columns.title
    elif sort == movie_sort_options.year:
        s = movies.columns.year
    elif sort == movie_sort_options.rating:
        s = desc(movies.columns.imdb_rating)
    else:
        s = movies.columns.title
    
    query = select(movies)

    if name != "":
        query = query.where(movies.c.title.ilike(f"%{name}%"))

    query = query.order_by(s, movies.c.movie_id).limit(limit).offset(offset)

    json = []
    with db.engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            json.append({
                "movie_id": row.movie_id,
                "movie_title": row.title,
                "year": row.year,
                "imdb_rating": row.imdb_rating,
                "imdb_votes": row.imdb_votes
            })
    return json
    
    # filtering out based on the name 
    if name != "":
        movList = [movie for movie in db.movies.values() if name in movie.title]
    else:
        movList = [movie for movie in db.movies.values() if movie.title is not None]

    if sort == movie_sort_options.movie_title:
        movList = sorted(movList, key=lambda x: x.title)
    elif sort == movie_sort_options.year:
        movList = sorted(movList, key=lambda x: x.year)
    elif sort == movie_sort_options.rating:
        movList = sorted(movList, key=lambda x: x.imdb_rating, reverse=True)
    
    json = []

    if limit > len(movList):
        limit = len(movList)

    for movie in movList[offset:offset + limit]:
        movieJson = {
            "movie_id": movie.movie_id,
            "movie_title": movie.title, 
            "year": movie.year,
            "imdb_rating": movie.imdb_rating,
            "imdb_votes": movie.imdb_votes
        }
        json.append(movieJson)

    # for i in range(offset, offset + limit):
    #     movieJson = {
    #         "movie_id": movList[i].movie_id,
    #         "movie_title": movList[i].title, 
    #         "year": movList[i].year,
    #         "imdb_rating": movList[i].imdb_rating,
    #         "imdb_votes": movList[i].imdb_votes
    #     }
    #     json.append(movieJson)


    return json
