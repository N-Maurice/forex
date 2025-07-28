#!/usr/bin/env python3

import os
import sys
import requests
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv("FMP_API_KEY.env")

print("Loading API key from FMP_API_KEY.env...")
api_key = os.getenv("FMP_API_KEY")

api_url = "?symbol=AAPL&apikey="

params = {
    "apikey": api_key
}

response = requests.get(api_url)
if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code, response.text)
