from sys import argv

def to_set(lst):
    return set(lst)

def call_center(clients, recipients):
    """Promo SMS olmagan mijozlar"""
    clinets_set = to_set(clients)
    recipients_set = to_set(recipients)
    return list(clinets_set - recipients_set)

def potential_clients(clients, participants):
    """Tadbir orasida ishtirokchi bo'lmaganlar"""
    clients_set = to_set(clients)
    participants_set = to_set(participants)
    return list(participants_set - clients_set)

def loyalty_program(clients, participants):
    """Tadbirda ishtirok etmaganlar"""
    clients_set = to_set(clients)
    participants_set = to_set(participants)
    return list(clients_set - participants_set)

def marketing(task):
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
        'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
        'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
        'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
        'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    if len(argv) !=2:
        return
    
    if task == "call_center":
        result = call_center(clients, recipients)
    elif task == "potential_clients":
        result = potential_clients(clients, participants)
    elif task == "loyalty_program":
        result = loyalty_program(clients,participants)
    else:
        raise ValueError("Please, give correct name!!!")

    for email in result:
        print(email)

if __name__ == "__main__":
    if len(argv) != 2:
        print("Error")    
    else: 
        marketing(argv[1])