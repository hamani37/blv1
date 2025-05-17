import requests
import numpy as np
import pandas as pd
import talib

def fetch_price_and_indicators(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["open"] = df["open"].astype(float)
    df["volume"] = df["volume"].astype(float)

    indicators = {
        "price": df["close"].iloc[-1],
        "rsi": float(talib.RSI(df["close"], timeperiod=14)[-1]),
        "macd": float(talib.MACD(df["close"])[0][-1]),
        "bollinger_upper": float(talib.BBANDS(df["close"])[0][-1]),
        "bollinger_middle": float(talib.BBANDS(df["close"])[1][-1]),
        "bollinger_lower": float(talib.BBANDS(df["close"])[2][-1]),
        "obv": float(talib.OBV(df["close"], df["volume"])[-1]),
        "vwap": float((df["volume"] * (df["high"] + df["low"] + df["close"]) / 3).sum() / df["volume"].sum()),
        "atr": float(talib.ATR(df["high"], df["low"], df["close"], timeperiod=14)[-1]),
    }

    return indicators
