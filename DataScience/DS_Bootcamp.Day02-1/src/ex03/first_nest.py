from sys import argv, exit 

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
        @staticmethod
        def counts(data):
            head_count = sum(row[0] for row in data)
            tail_count = sum(row[1] for row in data)
            return head_count, tail_count

        @staticmethod
        def fractions(head_count, tail_count):
            total = head_count + tail_count
            head_fraction = (head_count / total) * 100
            tail_fraction = (tail_count / total) * 100
            return head_fraction, tail_fraction

def main():
    if len(argv) != 2:
        exit("Input second argumment")

    filename = argv[1]
    research = Research(filename)

    data = research.file_reader(has_header=True)
    print(data)

    calculations = research.Calculations()
    head_count, tail_count = calculations.counts(data)
    print(head_count, tail_count)

    head_fraction, tail_fraction = calculations.fractions(head_count, tail_count)
    print(head_fraction, tail_fraction)

if __name__ == "__main__":
    main()



