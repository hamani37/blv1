import random

def log_signal(signal_type, price, features):
    rsi, macd, boll, obv = features
    color = "\033[92m" if rsi > 50 and macd > 0 else "\033[91m"
    reset = "\033[0m"
    print(f"{color}📈 Signal: {signal_type.upper()} | Prix: {price} | RSI: {rsi} | MACD: {macd} | Boll: {boll} | OBV: {obv}{reset}")
