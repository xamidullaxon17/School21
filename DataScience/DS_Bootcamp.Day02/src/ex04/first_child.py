from sys import argv, exit 
from random import randint


class Research:
    def __init__(self, filename):
        self.filename = filename

    def file_reader(self, has_header=True):
        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()

            if has_header:
                lines = lines[1:]

            data = []
            for line in lines:
                values = line.strip().split(",")
                if len(values) != 2 or not all(value in {"0", "1"} for value in values):
                    raise ValueError("Invalid file structures")
                data.append([int(value) for value in values])

            return data

        except FileNotFoundError:
            exit("File not found!")
        except Exception as e:
            exit(f"Error: {e}")


class Calculations:
    def __init__(self, data):
        self.data = data

    def counts(self):
        head_count = sum(row[0] for row in self.data)
        tail_count = sum(row[1] for row in self.data)
        return head_count, tail_count

    def fractions(self, head_count, tail_count):
        total = head_count + tail_count
        head_fraction = (head_count / total) * 100
        tail_fraction = (tail_count / total) * 100
        return head_fraction, tail_fraction

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        predictions = []
        for _ in range(num_predictions):
            predictions.append([1, 0] if randint(0, 1) == 1 else [0, 1])
        return predictions

    def predict_last(self):
        return self.data[-1]


def main():
    if len(argv) != 2:
        exit("Input second argumment")

    filename = argv[1]
    research = Research(filename)

    data = research.file_reader(has_header=True)
    print(data)

    analytics = Analytics(data)
    head_count, tail_count = analytics.counts()
    print(head_count, tail_count)

    head_fraction, tail_fraction = analytics.fractions(head_count, tail_count)
    print(head_fraction, tail_fraction)

    random_predictions = analytics.predict_random(3)
    print(random_predictions)

    last_prediction = analytics.predict_last()
    print(last_prediction)


if __name__ == "__main__":
    main()
