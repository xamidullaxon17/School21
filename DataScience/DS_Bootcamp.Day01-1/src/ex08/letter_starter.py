from sys import argv

def find_and_write_letter(email):
    try:
        with open('employees.tsv', 'r') as f:
            lines = f.readlines()[1:]
            email_name_map = {}
            
            for line in lines:
                name, _, e_mail = line.strip().split('\t')
                email_name_map[e_mail] = name
            
            if email in email_name_map:
                name = email_name_map[email]
                print(f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That's a precondition for the professionals that our company hires.")
            else:
                print("Email not found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python letter_starter.py <email>")
    else:
        find_and_write_letter(argv[1])
