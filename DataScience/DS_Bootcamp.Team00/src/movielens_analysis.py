import pytest
import os
import json
from movies import Movies
from links import Links
from tags import Tags
from ratings import Ratings, Movie_ratings, User_ratings

# Fixtures for common data
@pytest.fixture(scope="module")
def movie_data_file():
    file_path = 'test_movies.csv'
    data = """movieId,title,genres
1,Movie One (2001),Action|Comedy
2,Movie Two (2002),Drama|Romance
3,Movie Three (2003),Action|Thriller
4,Movie Four (2004),Action|Drama
5,Movie Five (2005),Comedy|Romance
6,"American President, The (1995)",Comedy|Drama|Romance
"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
    yield file_path
    os.remove(file_path)

@pytest.fixture
def sample_data(tmp_path):
    test_data = [
        {
            "movie_id": 1,
            "imdb_id": "0114709",
            "title": "Toy Story (1995)",
            "Director": "John Lasseter",
            "Budget": "$30,000,000 (estimated)",
            "Cumulative Worldwide Gross": "$394,436,586",
            "Runtime": "1 hour 21 minutes"
        },
        {
            "movie_id": 2,
            "imdb_id": "0113497",
            "title": "Jumanji (1995)",
            "Director": "Joe Johnston",
            "Budget": "$65,000,000 (estimated)",
            "Cumulative Worldwide Gross": "$262,821,940",
            "Runtime": "1 hour 44 minutes"
        },
        {
            "movie_id": 3,
            "imdb_id": "0113228",
            "title": "Grumpier Old Men (1995)",
            "Director": "Howard Deutch",
            "Budget": "$25,000,000 (estimated)",
            "Cumulative Worldwide Gross": "$71,518,503",
            "Runtime": "1 hour 41 minutes"
        },
        {
            "movie_id": 4,
            "imdb_id": "0114885",
            "title": "Waiting to Exhale (1995)",
            "Director": "Forest Whitaker",
            "Budget": "$16,000,000 (estimated)",
            "Cumulative Worldwide Gross": "$81,452,156",
            "Runtime": "2 hours 4 minutes"
        },
        {
            "movie_id": 5,
            "imdb_id": "0113041",
            "title": "Father of the Bride Part II (1995)",
            "Director": "Charles Shyer",
            "Budget": "$30,000,000 (estimated)",
            "Cumulative Worldwide Gross": "$76,594,107",
            "Runtime": "1 hour 46 minutes"
        }
    ]
    json_path = tmp_path / "test_links.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)
    return json_path

TEST_TAGS_CSV = "../datasets/tags.csv"
TEST_RATINGS_CSV = "../datasets/ratings.csv"
TEST_MOVIES_CSV = "../datasets/movies.csv"

@pytest.fixture
def sample_tags_file(): 
    yield TEST_TAGS_CSV  

@pytest.fixture
def sample_ratings_file():
    yield Ratings(TEST_RATINGS_CSV, TEST_MOVIES_CSV)

class TestMovies:
    def test_dist_by_release(self, movie_data_file):
        m = Movies(movie_data_file)
        assert m.dist_by_release() == {2001: 1, 2002: 1, 2003: 1, 2004: 1, 2005: 1, 1995: 1}

    def test_dist_by_genres(self, movie_data_file):
        m = Movies(movie_data_file)
        assert m.dist_by_genres() == {'Action': 3, 'Comedy': 3, 'Drama': 3, 'Romance': 3, 'Thriller': 1}

    def test_most_genres(self, movie_data_file):
        m = Movies(movie_data_file)
        assert m.most_genres(3) == {
            'American President, The (1995)': 3,
            'Movie One (2001)': 2,
            'Movie Two (2002)': 2
        }

class TestLinks:
    def test_top_directors(self, sample_data):
        l = Links("not_needed.csv")
        l.file = str(sample_data)
        assert l.top_directors(2) == {"John Lasseter": 1, "Joe Johnston": 1}

    def test_most_expensive(self, sample_data):
        l = Links("not_needed.csv")
        l.file = str(sample_data)
        assert l.most_expensive(2) == {
            "Jumanji (1995)": 65_000_000,
            "Toy Story (1995)": 30_000_000
        }

    def test_most_profitable(self, sample_data):
        l = Links("not_needed.csv")
        l.file = str(sample_data)
        assert l.most_profitable(2) == {
            "Toy Story (1995)": 364_436_586,
            "Jumanji (1995)": 197_821_940
        }

    def test_longest(self, sample_data):
        l = Links("not_needed.csv")
        l.file = str(sample_data)
        assert l.longest(2) == {
            "Waiting to Exhale (1995)": 124,
            "Father of the Bride Part II (1995)": 106
        }

    def test_top_cost_per_minute(self, sample_data):
        l = Links("not_needed.csv")
        l.file = str(sample_data)
        assert l.top_cost_per_minute(2) == {
            "Jumanji (1995)": round(65_000_000 / 104, 2),
            "Toy Story (1995)": round(30_000_000 / 81, 2)
        }

class TestTags:
    def test_most_words(self, sample_tags_file):
        tags = Tags(sample_tags_file)
        assert tags.most_words(10) == [
            ('funny', 15), ('sci-fi', 14), ('twist ending', 12), ('dark comedy', 12),
            ('atmospheric', 10), ('superhero', 10), ('comedy', 10), ('action', 10),
            ('suspense', 10), ('Leonardo DiCaprio', 9)
        ]

    def test_longest(self, sample_tags_file):
        tags = Tags(sample_tags_file)
        assert tags.longest(10) == [
            "Something for everyone in this one... saw it without and plan on seeing it with kids!",
            "the catholic church is the most corrupt organization in history",
            "audience intelligence underestimated",
            "Oscar (Best Music - Original Score)",
            "assassin-in-training (scene)",
            "Oscar (Best Cinematography)",
            "Everything you want is here",
            "political right versus left",
            "representation of children",
            "Guardians of the Galaxy"
        ]

    def test_tags_with(self, sample_tags_file):
        tags = Tags(sample_tags_file)
        assert tags.tags_with("oo") == [
            "High School", "Hollywood", "Orlando Bloom", "Poor story", "Woody Harrelson",
            "based on a book", "bloody", "cartoon", "comic book", "courtroom drama",
            "feel-good", "good dialogue", "good soundtrack", "good writing", "goofy",
            "high school", "highschool", "oldie but goodie", "poorly paced", "too long", "way too long"
        ]

    def test_most_words_and_longest(self, sample_tags_file):
        tags = Tags(sample_tags_file)
        assert tags.most_words_and_longest(10) == []

class TestMovieRatings:
    def test_top_avg_movies(self, sample_ratings_file):
        movies = Movie_ratings(sample_ratings_file)
        assert movies.top_by_ratings(10, metric='average') == {
            "Bottle Rocket (1996)": 5.0, "Canadian Bacon (1995)": 5.0,
            "Star Wars: Episode IV - A New Hope (1977)": 5.0,
            "James and the Giant Peach (1996)": 5.0, "Wizard of Oz": 5.0,
            "Citizen Kane (1941)": 5.0, "Adventures of Robin Hood": 5.0,
            "Mr. Smith Goes to Washington (1939)": 5.0,
            "Winnie the Pooh and the Blustery Day (1968)": 5.0,
            "Three Caballeros": 5.0
        }

    def test_top_med_movies(self, sample_ratings_file):
        movies = Movie_ratings(sample_ratings_file)
        assert movies.top_by_ratings(10, metric='median') == {
            "Bottle Rocket (1996)": 5.0, "Canadian Bacon (1995)": 5.0,
            "Star Wars: Episode IV - A New Hope (1977)": 5.0,
            "Tommy Boy (1995)": 5.0, "Forrest Gump (1994)": 5.0,
            "Fugitive": 5.0, "Jurassic Park (1993)": 5.0,
            "Tombstone (1993)": 5.0, "Dances with Wolves (1990)": 5.0,
            "Pinocchio (1940)": 5.0
        }

    def test_most_common_ratings(self, sample_ratings_file):
        movies = Movie_ratings(sample_ratings_file)
        assert movies.most_ratings(10) == {
            4.0: 292, 5.0: 267, 3.0: 253, 2.0: 57, 1.0: 39,
            4.5: 33, 0.5: 24, 3.5: 17, 1.5: 11, 2.5: 7
        }

    def test_dist_by_year(self, sample_ratings_file):
        movies = Movie_ratings(sample_ratings_file)
        assert movies.dist_by_year() == {
            1996: 358, 1999: 82, 2000: 296, 2001: 70,
            2005: 121, 2006: 4, 2007: 1, 2011: 39, 2015: 29
        }

    def test_top_controversial_movies(self, sample_ratings_file):
        movies = Movie_ratings(sample_ratings_file)
        assert movies.top_controversial(5) == {
            "Bambi (1942)": 5.06, "Rescuers": 5.06,
            "My Fair Lady (1964)": 5.06, "Matrix": 4.0,
            "Schindler's List (1993)": 3.42
        }

class TestUserRatings:
    def test_ratings_count_distribution(self, sample_ratings_file):
        users = User_ratings(sample_ratings_file)
        assert users.ratings_distribution() == {
            1: 232, 2: 29, 3: 39, 4: 216, 5: 44, 6: 314, 7: 126
        }

    def test_median_ratings_distribution(self, sample_ratings_file):
        users = User_ratings(sample_ratings_file)
        assert users.average_median_ratings_distribution(metric='median') == {
            1: 5.0, 2: 4.0, 3: 0.5, 4: 4.0, 5: 4.0, 6: 3.0, 7: 4.0
        }

    def test_avg_ratings_distribution(self, sample_ratings_file):
        users = User_ratings(sample_ratings_file)
        assert users.average_median_ratings_distribution(metric='average') == {
            1: 4.37, 2: 3.95, 3: 2.44, 4: 3.56, 5: 3.64, 6: 3.49, 7: 3.35
        }

    def test_top_variance_users(self, sample_ratings_file):
        users = User_ratings(sample_ratings_file)
        assert users.top_n_variance_users(10) == {
            3: 4.26, 4: 1.72, 7: 1.65, 5: 0.96,
            6: 0.72, 1: 0.64, 2: 0.63
        }