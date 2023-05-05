from dataclasses import dataclass


@dataclass
class Character:
    id: int
    name: str
    movie_id: int
    gender: str
    age: int
    num_lines: int


@dataclass
class Movie:
    id: int
    title: str
    year: int
    imdb_rating: float
    imdb_votes: int
    raw_script_url: str


@dataclass
class Conversation:
    id: int
    c1_id: int
    c2_id: int
    movie_id: int
    num_lines: int


@dataclass
class Line:
    id: int
    c_id: int
    movie_id: int
    conv_id: int
    line_sort: int
    line_text: str
