import os
import re
from collections import Counter

class Movies:
    """
    Analyzing data from movies.csv
    """ 
    def __init__(self, path_to_the_file):
        if not os.path.exists(path_to_the_file):
            raise FileNotFoundError(f"File '{path_to_the_file}' is not found.")

        self.movies = []
        with open(path_to_the_file, 'r', encoding='utf-8') as f:
            next(f)
            for i, line in enumerate(f):
                if i >= 1000:
                    break

                parts = line.strip().rsplit(',', 1)
                movie_id, title = parts[0].split(',', 1)

                genres = parts[-1]
                title = title.strip('"')
                self.movies.append({'movieId': int(movie_id), 'title': title, 'genres': genres.split('|')})

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        release_years = Counter()
        for movie in self.movies:
            match = re.findall(r'\((\d{4})\)', movie['title'])
            if match:
                year = int(match[-1])
                release_years[year] += 1

        sorted_years = sorted(release_years.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_years)

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genres = Counter()
        for movie in self.movies:
            for genre in movie['genres']:
                if genre == "(no genres listed)":
                    continue
                genres[genre] += 1
        sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_genres)

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        movies = Counter()
        for movie in self.movies:
            title = movie['title']
            num_genres = len(movie['genres'])
            movies[title] = num_genres

        return dict(movies.most_common(n))

