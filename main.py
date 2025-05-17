import time
import json
from flask import Flask, request
from log_utils import log_signal, print_stats
from ml_model import predict_signal, auto_train
from live_price import get_price_and_indicators, update_variation

app = Flask(__name__)
variation_tracker = {"last_price": None, "max": 0, "min": float("inf")}

@app.route("/")
def index():
    return "BLV Trading IA - Webhook en ligne"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    signal = data.get("signal")

    if not signal:
        return "Aucun signal", 400

    price_data = get_price_and_indicators()
    update_variation(price_data["price"], variation_tracker)

    result = {
        "signal": signal,
        **price_data,
        "variation_max": variation_tracker["max"],
        "variation_min": variation_tracker["min"]
    }

    log_signal(result)
    auto_train()

    print(f"\n📈 Signal: {signal} | Prix: {price_data['price']} | RSI: {price_data['rsi']} | MACD: {price_data['macd']} | "
          f"Boll: {price_data['boll']} | OBV: {price_data['obv']} | VWAP: {price_data['vwap']} | ATR: {price_data['atr']} | "
          f"SuperTrend: {price_data['supertrend']}")
    print(f"🟡 Variation max : {variation_tracker['max']} | Variation min : {variation_tracker['min']}")
    print_stats()

    return "Signal reçu", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
