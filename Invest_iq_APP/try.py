#!/usr/bin/env python3

"""
InvestIQ CLI Tool
Fetches:
- Government bond information
- Forex exchange rates
- Stock quotes

APIs used:
- Financial Modeling Prep
"""

import os
import sys
import requests
from dotenv import load_dotenv
from tabulate import tabulate

# ✅ Load API key from FMP_API_KEY.env
load_dotenv("FMP_API_KEY.env")
API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    print("❌ API Key not found! Please check FMP_API_KEY.env")
    sys.exit(1)

BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_bonds():
    print("\n📘 Fetching Government Bonds...")
    endpoint = f"{BASE_URL}/treasury?apikey={API_KEY}"
    res = requests.get(endpoint)
    if res.status_code == 200:
        bonds = res.json()
        if not bonds:
            print("⚠️ No bond data returned.")
            return
        table = [
            [
                b.get('symbol', 'N/A'),
                b.get('name', 'N/A'),
                b.get('country', 'N/A'),
                f"{b.get('yield', 'N/A')}%",
                b.get('maturityDate', 'N/A')
            ]
            for b in bonds[:10]
        ]
        print(tabulate(table, headers=["Symbol", "Name", "Country", "Yield", "Maturity"]))
    else:
        print("❌ Failed to fetch bond data.")

def get_forex():
    print("\n💱 Fetching Forex Exchange Rates (Base: USD)...")
    endpoint = f"{BASE_URL}/forex?apikey={API_KEY}"
    res = requests.get(endpoint)
    if res.status_code == 200:
        forex = res.json()
        if not forex:
            print("⚠️ No forex data available.")
            return
        table = [
            [f.get('ticker', 'N/A'), f.get('bid', 'N/A'), f.get('ask', 'N/A')]
            for f in forex[:10]
        ]
        print(tabulate(table, headers=["Pair", "Bid", "Ask"]))
    else:
        print("❌ Failed to fetch forex data.")

def get_stocks(symbols=["AAPL", "GOOG", "TSLA"]):
    print("\n📈 Fetching Stock Quotes...")
    joined = ",".join(symbols)
    endpoint = f"{BASE_URL}/quote/{joined}?apikey={API_KEY}"
    res = requests.get(endpoint)
    if res.status_code == 200:
        stocks = res.json()
        if not stocks:
            print("⚠️ No stock data returned.")
            return
        table = [
            [
                s.get('symbol', 'N/A'),
                s.get('name', 'N/A'),
                f"${s.get('price', 'N/A')}",
                f"{s.get('changesPercentage', 'N/A')}%"
            ]
            for s in stocks
        ]
        print(tabulate(table, headers=["Symbol", "Company", "Price", "Change"]))
    else:
        print("❌ Failed to fetch stock data.")

def main():
    print("💼 Welcome to InvestIQ CLI — Financial Market Insights\n")
    while True:
        print("\nChoose an option:")
        print("1. View Bond Market Data")
        print("2. View Forex Rates")
        print("3. View Stock Quotes")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            get_bonds()
        elif choice == "2":
            get_forex()
        elif choice == "3":
            symbols = input("Enter comma-separated stock symbols (e.g. AAPL,MSFT): ")
            symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
            if symbol_list:
                get_stocks(symbol_list)
            else:
                print("⚠️ No symbols entered.")
        elif choice == "4":
            print("👋 Exiting InvestIQ CLI. Goodbye!")
            break
        else:
            print("❌ Invalid input. Please try again.")

if __name__ == "__main__":
    main()
