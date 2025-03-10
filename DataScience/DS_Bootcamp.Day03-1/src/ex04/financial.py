#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
import time

def get_data(ticker: str, field):
    url = f"https://finance.yahoo.com/quote/{ticker}/financials/"
    try:
        response = requests.get(url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
        )
    except Exception as e:
        raise ValueError("Url not found")

    if response.status_code != 200:
        raise ValueError(
            f"Error: URL {ticker}  doesn't exist or not available. HTTP Status code: {response.status_code}"
        )

    soup = BeautifulSoup(response.text, "html.parser")

    table_fin_container = soup.find("section", class_="finContainer")

    if not table_fin_container:
        raise ValueError(f"There is no ticker ({ticker}) like that")
    table_body = table_fin_container.find("div", class_="tableBody")
    table_row = table_body.find_all("div", class_="row")

    field = field.lower()

    for r in table_row:
        res = tuple()
        f = r.find("div", class_="rowTitle").text.strip().lower()
        if f == field:
            for c in r.find_all("div", class_="column"):
                res += (c.text.strip(),)
            return res
    raise ValueError(f"There is no field ({field}) like that")

def main():
    if len(sys.argv) != 3:
        print("Usage: ./financial.py <ticker> <field_name>")
        sys.exit(1)

    ticker = sys.argv[1]
    field_name = sys.argv[2]

#    time.sleep(5)

    try:
        result = get_data(ticker, field_name)
        print(result)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
