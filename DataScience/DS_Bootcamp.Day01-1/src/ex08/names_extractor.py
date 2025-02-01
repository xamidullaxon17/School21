from sys import argv

def extract_names(file_path):
    try:
        with open(file_path, 'r') as f:
            emails = f.read().strip().split('\n')
        
        with open('employees.tsv', 'w') as output:
            output.write("Name\tSurname\tE-mail\n")
            
            for email in emails:
                name, surname = email.split('@')[0].split('.')
                name = name.capitalize()
                surname = surname.capitalize()
                output.write(f"{name}\t{surname}\t{email}\n")
        
        print("employees.tsv created successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(argv) != 2:
        print("Error")
    else:
        extract_names(argv[1])
