#!/usr/bin/env python3


"""
InvestIQ CLI Tool
Fetches:
- Government bond information
- Forex exchange rates

APIs used:
- Financial Modeling Prep
- JSONPlaceholder
"""

import os
import sys
import requests
from dotenv import load_dotenv
from tabulate import tabulate

# Load API key from the FMP_API_KEY.env file
load_dotenv("FMP_API_KEY.env")

# Load API key
load_dotenv()

def get_bonds(bond_type):
    print("\nFetching Government Bond Market Data...")

    url = f"https://bonds-ncd-fixed-income.p.rapidapi.com/Type?type={bond_type}"

    headers = {
	    "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
        "x-rapidapi-host": os.getenv("RAPID_API_HOST")
    }

    response = requests.get(url=url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        print("Failed to fetch bond data.")
        return
    
    bonds_d = response.json()
    table = [
        [
            f.get('id', 'N/A'),
            f.get('ISIN', 'N/A'),
            f.get('Expiry_Date', 'N/A'),
            f.get('Collateral', 'N/A'),
            f.get('Type', 'N/A')
            ] for f in bonds_d[:10]]

    print(tabulate(table, headers=["ID",
                                   "ISIN",
                                   "Expiry_Date",
                                   "Collateral",
                                   "Type"]))

def get_forex():
    print("\n💱 Fetching Forex Exchange Rates (Base: USD)...")
    api_url = f"https://financialmodelingprep.com/stable/forex-list?apikey={os.getenv('FMP_API_KEY')}"
    res = requests.get(api_url, timeout=15)
    if res.status_code == 200:
        forex = res.json()
        table = [
            [f['symbol'],
             f['fromCurrency'],
             f['toCurrency'],
             f['fromName'],
             f['toName']] for f in forex[:10]]
        print(tabulate(table, headers=["Symbol",
                                       "From Currency",
                                       "To Currency",
                                       "From Name",
                                       "To Name"]))
    else:
        print("Failed to fetch forex data.")

def get_stocks(symbols=["AAPL", "GOOG", "TSLA"]):
    print("\nFetching Stock Quotes...")
    joined = ",".join(symbols)
    api_url = "https://financialmodelingprep.com/stable/market-capitalization"
    params = {
        "symbol": joined,
        "apikey": os.getenv("FMP_API_KEY")
    }

    res = requests.get(url=api_url,
                       params=params,
                       timeout=10)
    
    if res.status_code != 200:
        print("Error fetching stock data:\n")
        print(res.text)
    
    stocks = res.json()
    table = [[s['symbol'], f"{s['date']}", f"{s['marketCap']}%"] for s in stocks]
    print(tabulate(table, headers=["Symbol", "Company", "Price", "Change"]))

def main():
    print("Welcome to InvestIQ CLI — Financial Market Insights\n")
    while True:
        print("\nChoose an option:")
        print("1. View Bond Market Data")
        print("2. View Forex Rates")
        print("3. View Stock Quotes")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            symbols = input("Enter comma-separated bond symbols (e.g. CB, SGB, GS, Tbill, MF, ETF): ").upper()
            get_bonds(bond_type=symbols)
        elif choice == "2":
            get_forex()
        elif choice == "3":
            symbols = input("Enter comma-separated stock symbols (e.g. AAPL,MSFT): ")
            get_stocks([s.strip().upper() for s in symbols.split(",") if s.strip()])
        elif choice == "4":
            print("Exiting InvestIQ CLI. Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
