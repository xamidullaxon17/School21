from sys import argv

def stocks():
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

    input_string = argv[1]
    if ",," in input_string:
        return
    expressions = [expr.strip() for expr in input_string.split(",")]

    for expr in expressions:
        if not expr:
            continue
        expr = expr.title()

        if  expr in COMPANIES:
            ticker = COMPANIES[expr]
            stock_price = STOCKS[ticker]
            print(f"{expr} stock price is {stock_price}")
        elif expr.upper() in STOCKS:
            company_name = [key for key, value in COMPANIES.items() if value == expr.upper()][0]
            print(f"{expr.upper()} is a ticker symbol for {company_name}")
        else:
            print(f"{expr} is an unknown company or an unknown ticker symbol")

if __name__ == "__main__":
    stocks()
