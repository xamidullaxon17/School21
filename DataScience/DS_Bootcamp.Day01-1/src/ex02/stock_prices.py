from sys import argv

def stock():
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
        }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
        }

    if len(argv) != 2:
        return 
    
    company_name = argv[1].capitalize()

    if company_name not in COMPANIES:
        print("Unknown company")
    else:
        company_code = COMPANIES[company_name]
        print(STOCKS[company_code])

if __name__ == "__main__":
    stock()








