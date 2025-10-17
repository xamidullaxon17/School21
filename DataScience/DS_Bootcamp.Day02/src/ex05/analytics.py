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

class Analytics(Research):
    def __init__(self, filename):
        super().__init__(filename)
        self.data = self.file_reader()

    def counts(self):
        heads = sum(row[0] for row in self.data)
        tails = sum(row[1] for row in self.data)
        return heads, tails
    
    def fractions(self, counts):
        total = sum(counts)
        return [(count / total) * 100 for count in counts]

    def predict_random(self, num_predictions):
        predictions = []
        for _ in range(num_predictions):
            predictions.append([1, 0] if randint(0,1) == 1 else [0,1])
        return predictions
    
    def predict_last(self):
        return self.data[-1]
    
    def save_file(self, data, filename, extension = "txt"):
        filepath = f"{filename}.{extension}"
        with open(filepath, "w") as f:
            f.write(data)
        return filepath
    
    




