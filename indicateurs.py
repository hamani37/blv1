import random

def get_all_indicators():
    return {
        "RSI": round(random.uniform(30, 70), 2),
        "MACD": round(random.uniform(-2, 2), 2),
        "BOLL": round(random.uniform(1, 2), 2),
        "OBV": round(random.uniform(5000, 10000), 2)
    }
