class Research:
    def __init__(self):
        self.filename = "data.csv"

    def file_reader(self):
        try:
            with open(self.filename, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return f"{self.filename} is not found!"
        except Exception:
            return f"Error: {Exception}"    
        

def main():
    research = Research()
    print(research.file_reader())

if __name__ == "__main__":
    main()
