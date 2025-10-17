import os
from collections import Counter

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


class Tags:
    def __init__(self, path_to_the_file, limit=1000):
        self.path = path_to_the_file
        self.limit = 1000
        self.tag_index = None

    def _open_file(self):
        """ Helper method to open the CSV file and handle errors. """
        if not os.path.exists(self.path):
            print(f"Error: The file at {self.path} does not exist.")
            return None

        try:
            with open(self.path, 'r', encoding='utf-8') as file: 
                header = file.readline().strip().split(',')
                self.tag_index = header.index('tag') if 'tag' in header else None

                if self.tag_index is None:
                    print("Error: The 'tag' column is missing from the CSV file.")
                    return None 
                rows = []
                for i, line in enumerate(file):
                    if i >= self.limit:
                        break 
                    rows.append(line.strip().split(','))
                    
                return rows, self.tag_index   
        except Exception as e:
            print(f"Error: An unexpected error occurred while opening the file - {e}")
            return None


    def most_words(self, n):
        """Returns the top-n most common tags."""
        tag_counts = Counter()

        result = self._open_file()
        if result is None:
            return []

        rows, tag_index = result

        for row in rows:
            if len(row) > tag_index:
                tag = row[tag_index].strip()
                tag_counts[tag] += 1

        sorted_tags = tag_counts.most_common(n)
        return sorted_tags

    def longest(self, n):
        """Returns the top-n longest tags based on the number of characters."""
        tag_lengths = {}

        result = self._open_file()
        if result is None:
            return []

        rows, tag_index = result

        for row in rows:
            if len(row) > tag_index:
                tag = row[tag_index].strip()
                tag_lengths[tag] = len(tag)

        sorted_tags = sorted(tag_lengths.keys(), key=lambda x: tag_lengths[x], reverse=True)
        return sorted_tags[:n]
    
    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        unique_tags = set()
        
        result = self._open_file()
        if result is None:
            return []

        rows, tag_index = result

        for row in rows:
            if len(row) > tag_index:
                tag = row[tag_index].strip()
                if word.lower() in tag.lower():
                    unique_tags.add(tag)

        return sorted(unique_tags)

    def most_words_and_longest(self, n):
        """
        Returns the intersection of the top-n most frequent tags and top-n longest tags.
        """
        most_common = {tag for tag, _ in self.most_words(n)}
        longest_tags = set(self.longest(n))
        return sorted(most_common & longest_tags)

    def most_popular(self, n):
        """
        Returns a dictionary of the most popular tags (most frequent tags).
        Sorted by the count of occurrences in descending order.
        """
        tag_counts = Counter()

        result = self._open_file()
        if result is None:
            return {}

        rows, tag_index = result

        for row in rows:
            if len(row) > tag_index:
                tag = row[tag_index].strip()
                tag_counts[tag] += 1

        return dict(tag_counts.most_common(n))



# Fayl yo'lini kiritasiz (CSV fayl)
path = '../datasets/tags.csv'  # Fayl yo'li sizda boshqacha bo'lishi mumkin

# Tags obyektini yaratamiz
tags = Tags(path)

# most_words_and_longest funksiyasini chaqiramiz
natija = tags.most_words_and_longest(10)  # eng ko'p uchraydigan va eng uzun 10 taglar kesishmasi

# Natijani chiqaramiz
print_data(natija, "Top 10 frequent and longest tags (intersection)")
