import datetime

def log_signal(signal):
    print(f"[SIGNAL] {datetime.datetime.now()} | {signal['direction'].upper()} at {signal['price']}")

def log_decision(result):
    print(f"[IA] {datetime.datetime.now()} | Decision: {result['decision']} | Variation: {result['variation']}% | RSI: {result['rsi']} | MACD: {result['macd']}")
