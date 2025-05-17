import ta
import pandas as pd

def analyse_signal_ia(df):
    df = df.copy()
    df["close"] = df["close"].astype(float)

    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"]).rsi()
    df["macd"] = ta.trend.MACD(close=df["close"]).macd_diff()
    df["bb_upper"] = ta.volatility.BollingerBands(close=df["close"]).bollinger_hband()
    df["bb_lower"] = ta.volatility.BollingerBands(close=df["close"]).bollinger_lband()
    df["obv"] = ta.volume.OnBalanceVolumeIndicator(close=df["close"], volume=df["volume"]).on_balance_volume()

    last = df.iloc[-1]

    explanation = f"RSI={last['rsi']:.2f}, MACD={last['macd']:.4f}, OBV={last['obv']:.2f}"
    decision = "NEUTRE"

    if last["rsi"] < 30 and last["macd"] > 0 and last["close"] < last["bb_lower"]:
        decision = "LONG"
    elif last["rsi"] > 70 and last["macd"] < 0 and last["close"] > last["bb_upper"]:
        decision = "SHORT"

    return {
        "decision": decision,
        "explanation": explanation
    }
