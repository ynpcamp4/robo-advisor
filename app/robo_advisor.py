# app/robo_advisor.py

import csv
import json
import os 

from dotenv import load_dotenv
import requests

print("Welcome to Robo Advisor by Payam Daniel Abbassian")
print()
print("** This app is not intended to be investment advice. Seek a duly licensed professional for investment advice. **")
print()
symbol = input("To begin, please enter a ticker symbol: ")


def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
# V18VJTG4P4VS9OWV

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
print ("URL:", request_url)

response = requests.get(request_url)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

latest_open = tsd[latest_day]["1. open"]

import datetime
x = datetime.datetime.now ()

high_prices = []
low_prices  = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"] 

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
            })

x = float(latest_close)
y = float(latest_open)

if x >= y:
    recommendation = "BUY"
    recommendation_reason = "The price of the stock increased. Things look good."
else:
    recommendation = "SELL"
    recommendation_reason = "The price of the stock decreased. Things aren't looking so good."

print("-------------------------")
print("SELECTED SYMBOL:", symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA")
print("REQUEST AT:", x)
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION:" + recommendation)
print("RECOMMENDATION REASON:" + recommendation_reason)
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("GOOD LUCK!")
print("-------------------------")
