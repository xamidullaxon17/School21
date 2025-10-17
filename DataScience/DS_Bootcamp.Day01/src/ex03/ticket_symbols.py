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
    
    company_stock = argv[1].upper()
    
    if company_stock not in STOCKS:
        print("Unknown ticker")
    else:
        company_name = [key for key, value in COMPANIES.items() if value == company_stock][0]
        print(f"{company_name} {STOCKS[company_stock]}")

if __name__ == "__main__":
    stock()