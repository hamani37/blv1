import requests
import random

def get_price_and_indicators():
    price = round(get_binance_price(), 2)

    # Données factices à remplacer par vraies fonctions si besoin
    return {
        "price": price,
        "rsi": round(random.uniform(30, 70), 2),
        "macd": round(random.uniform(-2, 2), 2),
        "boll": round(random.uniform(0.5, 2), 2),
        "obv": round(random.uniform(5000, 10000), 2),
        "vwap": round(random.uniform(price - 1, price + 1), 2),
        "atr": round(random.uniform(0.5, 2), 2),
        "supertrend": round(random.choice([1, -1]), 2),
    }

def get_binance_price(symbol="SOLUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    return float(response.json()["price"])

def update_variation(current_price, tracker):
    if tracker["last_price"] is None:
        tracker["last_price"] = current_price
        tracker["max"] = current_price
        tracker["min"] = current_price
    else:
        tracker["max"] = max(tracker["max"], current_price)
        tracker["min"] = min(tracker["min"], current_price)
        tracker["last_price"] = current_price
