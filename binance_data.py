import requests
import time

def fetch_binance_price():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT")
        return float(response.json()["price"])
    except:
        return None

def start_price_tracking(price_data):
    while True:
        price = fetch_binance_price()
        if price:
            price_data.append(price)
            if len(price_data) > 300:
                price_data.pop(0)
        time.sleep(1)

def get_price_stats(price_data):
    if not price_data:
        return {"last": None, "high": None, "low": None, "rsi": None, "macd": None, "boll": None, "obv": None}

    last = price_data[-1]
    high = max(price_data)
    low = min(price_data)
    # Simples placeholders, à remplacer si on veut calculer les vrais indicateurs
    return {
        "last": round(last, 2),
        "high": round(high, 2),
        "low": round(low, 2),
        "rsi": round(50 + (last - low) / (high - low + 1e-6) * 50, 2),
        "macd": round((last - sum(price_data[-10:]) / 10), 2),
        "boll": round((high - low), 2),
        "obv": round(sum(price_data[-20:]) / len(price_data[-20:]), 2)
    }
