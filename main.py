from flask import Flask, request, jsonify
from ml_model import analyse_signal_ia
from log_utils import log_with_color, save_signal_data
import requests
import time
import threading
import pandas as pd
import datetime
import os

app = Flask(__name__)
live_data = []
symbol = "BTC/USDT"

def fetch_live_data():
    global live_data
    while True:
        try:
            response = requests.get(f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100")
            data = response.json()
            df = pd.DataFrame(data, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            df = df.astype(float)
            live_data = df
        except Exception as e:
            print("Erreur récupération live data:", e)
        time.sleep(1)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    signal_type = data.get("signal")
    price = float(data.get("price", 0))
    timestamp = datetime.datetime.now().isoformat()

    if live_data is None or len(live_data) == 0:
        return jsonify({"error": "Live data not ready"}), 503

    indicators = analyse_signal_ia(live_data.copy())
    decision, explanation = indicators["decision"], indicators["explanation"]
    log_with_color(signal_type, price, decision, explanation)
    save_signal_data(signal_type, price, decision, explanation, timestamp)

    return jsonify({"status": "Signal reçu", "decision": decision, "explanation": explanation}), 200

if __name__ == '__main__':
    threading.Thread(target=fetch_live_data, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
