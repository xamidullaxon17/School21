import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import json
import os

class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path):
        self.path = path
        self.file = "movies_data.json"
        self.datas = {}
        self.movie_titles = {}
        self.limit = 1001

    def get_imdb(self, list_of_movies, list_of_fields=["movie_id", "title", "Director", "imdb_id", "Budget", "Cumulative Worldwide Gross", "Runtime"]):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """        
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                self.datas = {movie["movie_id"]: movie for movie in json.load(f)}
        else:
            try:
                with open("../datasets/movies.csv", "r", encoding="utf-8") as f:
                    next(f)
                    for i, line in enumerate(f):
                        if i >= self.limit:
                            break
                        parts = line.strip().rsplit(',', 1)
                        movie_id, title = parts[0].split(',', 1)
                        title = title.strip('"')
                        self.movie_titles[int(movie_id)] = title
            except FileNotFoundError:
                pass

            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                    headers = lines[0].split(',')

                    for i, line in enumerate(lines[1:]):
                        if i >= self.limit:
                            break

                        movie_entry = dict(zip(headers, line.split(',')))
                        movie_id = int(movie_entry['movieId'])
                        imdb_id = movie_entry['imdbId'].zfill(7)
                        url = f'https://www.imdb.com/title/tt{imdb_id}/'

                        try:
                            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                            response.raise_for_status()
                            soup = BeautifulSoup(response.text, 'html.parser')
                        except requests.exceptions.RequestException:
                            continue

                        extracted_data = {
                            "movie_id": movie_id,
                            "imdb_id": imdb_id,
                            "title": self.movie_titles.get(movie_id, "N/A"),
                            "Director": "N/A",
                            "Budget": "N/A",
                            "Cumulative Worldwide Gross": "N/A",
                            "Runtime": "N/A"
                        }

                        director_section = soup.find("li", attrs={"data-testid": "title-pc-principal-credit"})
                        if director_section:
                            director_tag = director_section.find("a")
                            if director_tag:
                                extracted_data["Director"] = director_tag.text.strip()

                        budget_section = soup.find("li", attrs={"data-testid": "title-boxoffice-budget"})
                        if budget_section:
                            budget_value = budget_section.find("span", class_="ipc-metadata-list-item__list-content-item")
                            if budget_value:
                                extracted_data["Budget"] = budget_value.text.strip()

                        gross_section = soup.find("li", attrs={"data-testid": "title-boxoffice-cumulativeworldwidegross"})
                        if gross_section:
                            gross_value = gross_section.find("span", class_="ipc-metadata-list-item__list-content-item")
                            if gross_value:
                                extracted_data["Cumulative Worldwide Gross"] = gross_value.text.strip()

                        runtime_section = soup.find("li", attrs={"data-testid": "title-techspec_runtime"})
                        if runtime_section:
                            runtime_value = runtime_section.find("div", class_="ipc-metadata-list-item__content-container")
                            if runtime_value:
                                extracted_data["Runtime"] = runtime_value.text.strip()

                        self.datas[movie_id] = extracted_data

                try:
                    with open(self.file, "w", encoding="utf-8") as f:
                        json.dump(list(self.datas.values()), f, ensure_ascii=False, indent=4)
                except IOError:
                    pass

            except FileNotFoundError:
                pass

        result = []
        for movie_id in list_of_movies:
            if movie_id in self.datas:
                movie_data = self.datas[movie_id]
                selected_data = [movie_data.get(field, "N/A") for field in list_of_fields]
                result.append(selected_data)

        return result

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}

        directors_counter = Counter()

        for movie in data:
            director = movie.get("Director", "N/A")
            if director != "N/A":
                directors_counter[director] += 1

        directors_count = dict(directors_counter.most_common(n))

        return directors_count

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}

        budgets = Counter()

        clean_budget = lambda b: int(re.sub(r"[^\d]", "", re.sub(r"\(.*?\)", "", b))) if b and re.sub(r"[^\d]", "", b).isdigit() else 0

        for movie in data:
            movie_name = movie.get("title", "N/A")
            budget_text = movie.get("Budget", "N/A")
            budgett = clean_budget(budget_text)

            if movie_name != "N/A" and budgett > 0:
                budgets[movie_name] = budgett

        budget = dict((key, value) for key, value in budgets.most_common(n) if isinstance(value, int))

        return budget

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """        
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}

        profits = Counter()

        clean = lambda b: int(re.sub(r"[^\d]", "", re.sub(r"\(.*?\)", "", b))) if b and re.sub(r"[^\d]", "", b).isdigit() else 0

        for movie in data:
            movie_name = movie.get("title", "N/A")
            budget_text = movie.get("Budget", "N/A")
            gross_text = movie.get("Cumulative Worldwide Gross", "N/A")
            
            budget = clean(budget_text)
            gross = clean(gross_text)

            if movie_name != "N/A" and budget > 0 and gross > 0:
                profits[movie_name] = gross - budget
        
        return dict((key, value) for key, value in profits.most_common(n) if isinstance(value, int))

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version - choose any.
        Sort it by runtime descendingly.
        """
        runtimes = Counter()

        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}

        for movie in data:
            movie_name = movie.get("title", "N/A")
            runtime_text = movie.get("Runtime", "N/A")

            matches = re.findall(r"\d+", runtime_text)
            hours = int(matches[0]) if len(matches) > 0 else 0
            minutes = int(matches[1]) if len(matches) > 1 else 0
            runtime = hours * 60 + minutes

            if movie_name != "N/A" and runtime > 0:
                runtimes[movie_name] = runtime

        return dict(runtimes.most_common(n))

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies - do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        costs = Counter()

        try:
            with open(self.file, 'r', encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return {}

        clean_budget = lambda b: int(re.sub(r"[^\d]", "", re.sub(r"\(.*?\)", "", b))) if b and re.sub(r"[^\d]", "", b).isdigit() else 0

        for movie in data:
            movie_name = movie.get("title", "N/A")
            budget_text = movie.get("Budget", "N/A")
            runtime_text = movie.get("Runtime", "N/A")

            matches = re.findall(r"\d+", runtime_text)
            hours = int(matches[0]) if len(matches) > 0 else 0
            minutes = int(matches[1]) if len(matches) > 1 else 0
            runtime = hours * 60 + minutes

            budget = clean_budget(budget_text)

            if movie_name != "N/A" and budget > 0 and runtime > 0:
                cost = round(budget / runtime, 2)
                costs[movie_name] = cost

        return dict(costs.most_common(n))



# def get_imdb_id():
#     movie_id = []
#     with open("../datasets/links.csv", "r", encoding="utf-8") as f:
#         lines = f.read().splitlines()
#         for line in lines[1:1001]:
#             movie = int(line.split(",")[0])
#             movie_id.append(movie)
#     return movie_id
# all_id = get_imdb_id()