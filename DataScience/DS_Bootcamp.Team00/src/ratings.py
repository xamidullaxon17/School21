import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from statistics import median

def print_data(data, title):
    print(f"{title}:")
    if isinstance(data, dict):
        for key, value in data.items():
            print(key, ":", round(value, 2) if isinstance(value, float) else value)
    elif isinstance(data, list):
        for item in data:
            print(item[0], ":", round(item[1], 2) if isinstance(item[1], float) else item[1])
    elif isinstance(data, tuple):
        for item in data:
            print(item[0], ":", round(item[1], 2) if isinstance(item[1], float) else item[1])
    print()

class Ratings:
    def __init__(self, path_to_the_ratings_file, path_to_the_movies_file):
        self.ratingsFile = os.path.join(path_to_the_ratings_file)
        self.moviesFile = os.path.join(path_to_the_movies_file)
        self.limit = 1000
        self.movies = self._load_movies()
        self.ratings_data = self._load_ratings_data()

    def _load_movies(self):
        movies = {}
        if not os.path.exists(self.moviesFile):
            print(f"Error: Movies file not found at {self.moviesFile}.")
            return None
        try:
            with open(self.moviesFile, 'r', encoding='utf-8') as file:
                file.readline()
                for line in file:
                    movie_data = line.strip().split(',')
                    movie_id = int(movie_data[0])
                    title = movie_data[1]
                    movies[movie_id] = title
            return movies
        except FileNotFoundError:
            print(f"Error: Could not find movies file: {self.moviesFile}")
            return None
        except UnicodeDecodeError:
            print(f"Error: Encoding issue reading movies file: {self.moviesFile}")
            return None
        except Exception as e:
            print(f"Error: Unexpected error loading movies: {e}")
            return None

    def _load_ratings_data(self):
        if not os.path.exists(self.ratingsFile):
            print(f"Error: Ratings file not found at {self.ratingsFile}.")
            return None
        try:
            with open(self.ratingsFile, 'r', encoding='utf-8') as file:
                header = file.readline().strip().split(',')
                rows = []
                for i, line in enumerate(file):
                    if i >= self.limit:
                        break
                    rows.append(line.strip().split(','))
                return rows
        except FileNotFoundError:
            print(f"Error: Could not find ratings file: {self.ratingsFile}")
            return None
        except UnicodeDecodeError:
            print(f"Error: Encoding issue reading ratings file: {self.ratingsFile}")
            return None
        except Exception as e:
            print(f"Error: Unexpected error loading ratings: {e}")
            return None

    def fetch_movie_title(self, movie_id):
        title = self.movies.get(movie_id, "Unknown Movie")
        return title.strip('"') 

class Movie_ratings:
    def __init__(self, ratings):
        self.ratings = ratings

    def most_ratings(self, n):
        if self.ratings.ratings_data is None:
            return {}
        rating_counts = Counter()
        for row in self.ratings.ratings_data:
            rating = row[2]
            rating_counts[rating] += 1 
        return {float(key): value for key, value in rating_counts.most_common(n)}


    def dist_by_year(self):
        if self.ratings.ratings_data is None:
            return {}
        ratings_by_year = Counter()
        for row in self.ratings.ratings_data:
            timestamp = int(row[3])
            year = datetime.fromtimestamp(timestamp, tz=timezone.utc).year
            ratings_by_year[year] += 1
        return dict(sorted(ratings_by_year.items()))

    def dist_by_rating(self):
        if self.ratings.ratings_data is None:
            return {}
        ratings_distribution = Counter()
        for row in self.ratings.ratings_data:
            rating = row[2]
            ratings_distribution[rating] += 1
        return dict(sorted(ratings_distribution.items()))

    def top_by_ratings(self, n, metric):
        if self.ratings.ratings_data is None:
            return {}
        movie_ratings = defaultdict(list)
        for row in self.ratings.ratings_data:
            movie_id = int(row[1])
            rating = float(row[2])
            movie_ratings[movie_id].append(rating)
        sorted_movies = {}
        for movie_id, ratings_list in movie_ratings.items():
            if metric == 'average':
                sorted_movies[movie_id] = round(sum(ratings_list) / len(ratings_list), 2)
            elif metric == 'median':
                sorted_movies[movie_id] = round(median(ratings_list), 2)
            else:
                raise ValueError("Invalid metric. Use 'average' or 'median'.")
        sorted_movies = dict(sorted(sorted_movies.items(), key=lambda x: x[1], reverse=True))
        return {self.ratings.fetch_movie_title(movie_id): metric_value for movie_id, metric_value in list(sorted_movies.items())[:n]}

    def top_controversial(self, n):
        if self.ratings.ratings_data is None:
            return {}
        movie_ratings = defaultdict(list)
        for row in self.ratings.ratings_data:
            movie_id = int(row[1])
            rating = float(row[2])
            movie_ratings[movie_id].append(rating)
        movie_variance = {}
        for movie_id, ratings_list in movie_ratings.items():
            if len(ratings_list) > 1:
                mean = sum(ratings_list) / len(ratings_list)
                variance = sum((x - mean) ** 2 for x in ratings_list) / len(ratings_list)
                movie_variance[movie_id] = round(variance, 2)
            else:
                movie_variance[movie_id] = 0.0
        sorted_movies = dict(sorted(movie_variance.items(), key=lambda x: x[1], reverse=True))
        return {self.ratings.fetch_movie_title(movie_id): variance for movie_id, variance in list(sorted_movies.items())[:n]}

class User_ratings:
    def __init__(self, ratings):
        self.ratings = ratings

    def ratings_distribution(self):
        if self.ratings.ratings_data is None:
            return {}
        user_ratings_count = Counter()
        for row in self.ratings.ratings_data:
            user_id = int(row[0])
            user_ratings_count[user_id] += 1
        return dict(user_ratings_count)

    def average_median_ratings_distribution(self, metric='average'):
        if self.ratings.ratings_data is None:
            return {}
        user_ratings = defaultdict(list)
        for row in self.ratings.ratings_data:
            user_id = int(row[0])
            rating = float(row[2])
            user_ratings[user_id].append(rating)
        user_ratings_metric = {}
        for user_id, ratings_list in user_ratings.items():
            if metric == 'average':
                user_ratings_metric[user_id] = round(sum(ratings_list) / len(ratings_list), 2)
            elif metric == 'median':
                user_ratings_metric[user_id] = round(median(ratings_list), 2)
            else:
                raise ValueError("Invalid metric. Choose 'average' or 'median'.")
        return user_ratings_metric

    def top_n_variance_users(self, n=10):
        if self.ratings.ratings_data is None:
            return {}
        user_ratings = defaultdict(list)
        for row in self.ratings.ratings_data:
            user_id = int(row[0])
            rating = float(row[2])
            user_ratings[user_id].append(rating)
        user_variances = {}
        for user_id, ratings_list in user_ratings.items():
            if len(ratings_list) > 1:
                mean = sum(ratings_list) / len(ratings_list)
                variance = sum((x - mean) ** 2 for x in ratings_list) / len(ratings_list)
                user_variances[user_id] = round(variance, 2)
            else:
                user_variances[user_id] = 0
        sorted_users = sorted(user_variances.items(), key=lambda x: x[1], reverse=True)[:n]
        return dict(sorted_users)
