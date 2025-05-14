# utils/indicateurs.py

import requests

def recuperer_prix_binance_et_indicateurs(type_signal):
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT")
        price = float(response.json()["price"])
    except:
        return None

    # Simule les indicateurs pour le moment
    rsi = 58.95
    macd = -0.58 if type_signal == "short" else 0.42
    bollinger = 1.38
    obv = 6416.2

    return {
        "price": price,
        "rsi": rsi,
        "macd": macd,
        "bollinger": bollinger,
        "obv": obv
    }
