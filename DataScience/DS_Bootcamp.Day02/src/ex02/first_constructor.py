from sys import argv

class Research:
    def __init__(self,argument):
        self.filename = argument

    def file_reader(self):
        try:
            with open(self.filename, "r") as f:
                lines =  f.readlines()
                if not lines:
                    raise ValueError("File is empty or missing header")

                header = lines[0].strip().split(",")
                if len(header) != 2:
                    raise ValueError("Header must be given two strings delimited by a comma")
                
                for line in lines[1:]:
                    values = line.strip().split(",")
                    if len(values) != 2 or not all(value in {"0","1"} for value in values):
                        raise ValueError("Rows must contain exactly two values (0 or 1) delimited by a comma")

                return "".join(lines).strip()  


        except FileNotFoundError:
            return "File not found!"
        except Exception as e:
            return f"Error {e}"

def main():
    if len(argv) != 2:
        print("Input second argument")
        return
    
    data = argv[1]
    file = Research(data)
    print(file.file_reader())

if __name__ == "__main__":
    main()

