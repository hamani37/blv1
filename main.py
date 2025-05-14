import json
import time
import threading
from flask import Flask, request
from ml_model import process_signal
from logbook import log_signal_info
from binance_data import start_price_tracking, get_price_stats

app = Flask(__name__)
price_data = []
signal_history = []

# Démarre le suivi du prix en live dans un thread séparé
threading.Thread(target=start_price_tracking, args=(price_data,), daemon=True).start()

@app.route("/", methods=["GET"])
def home():
    return "API active"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    signal_type = data.get("type")
    if signal_type not in ["long", "short"]:
        return "Signal invalide", 400

    signal_history.append({"type": signal_type, "timestamp": time.time(), "price": get_price_stats(price_data)["last"]})

    indicators = get_price_stats(price_data)
    log_signal_info(signal_type, indicators)
    response = process_signal(signal_type, indicators)

    return json.dumps({"status": "ok", "response": response})

if __name__ == "__main__":
    app.run(debug=True)
