#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask_caching import Cache
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv("FMP_API_KEY.env")

# Cache config — store in memory for 24 hours
#app.config['CACHE_TYPE'] = 'SimpleCache'

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'redis'
app.config['CACHE_REDIS_PORT'] = 6379

app.config['CACHE_DEFAULT_TIMEOUT'] = 86400
cache = Cache(app)

FMP_API_KEY = os.getenv("FMP_API_KEY")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/get-bonds", methods=["POST"])
def get_bonds():
    bond_type = request.form.get("bondType", "").upper()
    cache_key = f"bonds_{bond_type}"
    data = cache.get(cache_key)

    if data is None:
        url = f"https://bonds-ncd-fixed-income.p.rapidapi.com/Type?type={bond_type}"
        headers = {
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": RAPID_API_HOST
        }
        response = requests.get(url, headers=headers, timeout=10)
        data = []

        if response.status_code == 200:
            try:
                bonds = response.json()
                if isinstance(bonds, list):
                    for b in bonds[:100]:  # Limit to 100 bonds
                        data.append({
                            "issuer_name": b.get("Issuer_Name", "Unknown"),
                            "name": b.get("ISIN", "Unknown"),
                            "yield": b.get("Hair_Cut", "N/A"),
                            "date": b.get("Expiry_Date", "N/A")
                        })
                cache.set(cache_key, data)
            except Exception as e:
                print("Error processing bonds:", e)

    return render_template("display.html", bonds=data, forex=[], todos=[])


@app.route("/get-forex", methods=["POST"])
def get_forex():
    cache_key = "forex_data"
    data = cache.get(cache_key)

    if data is None:
        url = f"https://financialmodelingprep.com/api/v3/forex?apikey={FMP_API_KEY}"
        response = requests.get(url, timeout=10)
        data = []

        if response.status_code == 200:
            try:
                json_data = response.json()

                if isinstance(json_data, list):
                    forex_data = json_data
                elif isinstance(json_data, dict) and 'forexList' in json_data:
                    forex_data = json_data['forexList']
                else:
                    forex_data = []

                for f in forex_data[:10]:
                    data.append({
                        "pair": f.get("ticker") or f.get("symbol") or "N/A",
                        "rate": f.get("bid") or f.get("price") or "N/A",
                        "timestamp": f.get("timestamp", "N/A")
                    })
                cache.set(cache_key, data)
            except Exception as e:
                print("Error processing forex:", e)

    return render_template("display.html", bonds=[], forex=data, todos=[])


@app.route("/get-stocks", methods=["POST"])
def get_stocks():
    cache_key = "stock_todos"
    todos = cache.get(cache_key)

    if todos is None:
        symbols = request.form.get("stockSymbols", "")
        url = f"https://jsonplaceholder.typicode.com/todos"
        response = requests.get(url, timeout=10)
        todos = []

        if response.status_code == 200:
            try:
                json_data = response.json()
                for t in json_data[:10]:
                    todos.append({
                        "employee": f"User {t['userId']}",
                        "title": t['title'],
                        "completed": t['completed']
                    })
                cache.set(cache_key, todos)
            except Exception as e:
                print("Error processing todos:", e)

    return render_template("display.html", bonds=[], forex=[], todos=todos)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
