from statistics import mean
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
from ta.trend import CCIIndicator
import pandas as pd

def analyse_signal(signal, history):
    if len(history) < 5:
        return {"status": "waiting", "reason": "not enough history"}

    df = pd.DataFrame(history)
    df["price"] = pd.to_numeric(df["price"])
    close = df["price"]

    rsi = RSIIndicator(close).rsi().iloc[-1]
    macd = MACD(close).macd_diff().iloc[-1]
    bb = BollingerBands(close)
    bb_width = bb.bollinger_hband().iloc[-1] - bb.bollinger_lband().iloc[-1]
    obv = OnBalanceVolumeIndicator(close, pd.Series([1000000]*len(close))).on_balance_volume().iloc[-1]
    cci = CCIIndicator(close).cci().iloc[-1]

    last_price = float(signal["price"])
    last_dir = signal["direction"]
    previous_price = float(history[-1]["price"])
    variation = ((last_price - previous_price) / previous_price) * 100

    valid_long = last_dir == "long" and variation > 0.5
    valid_short = last_dir == "short" and variation < -0.5

    if valid_long:
        decision = "SEND_LONG"
    elif valid_short:
        decision = "SEND_SHORT"
    else:
        decision = "REJECTED"

    return {
        "timestamp": signal["timestamp"],
        "pair": signal["pair"],
        "interval": signal["interval"],
        "price": last_price,
        "direction": last_dir,
        "variation": round(variation, 3),
        "rsi": round(rsi, 2),
        "macd": round(macd, 4),
        "bb_width": round(bb_width, 4),
        "obv": round(obv, 2),
        "cci": round(cci, 2),
        "decision": decision
    }
