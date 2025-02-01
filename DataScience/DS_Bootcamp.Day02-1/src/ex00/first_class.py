class Must_read():
    def __init__(self):
        self.filename = "data.csv"

    def read(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    print(line.strip())
        except FileNotFoundError:
            print(f"{self.filename} isn't found!")
        except Exception:
            print("Error")

def main():
    pir = Must_read()
    pir.read()
    
if __name__ == "__main__":
    main()