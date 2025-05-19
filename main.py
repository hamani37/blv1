from flask import Flask, request, jsonify
from ml_model import analyse_signal
from log_utils import log_signal, log_decision
import json
import time

app = Flask(__name__)

PAIR = "SOL/USDT"
INTERVAL = "1m"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    with open("live_data.json", "r") as f:
        history = json.load(f)

    signal = {
        "timestamp": time.time(),
        "pair": PAIR,
        "interval": INTERVAL,
        "price": data.get("price"),
        "direction": data.get("signal")
    }

    log_signal(signal)
    result = analyse_signal(signal, history)

    log_decision(result)
    history.append(result)
    with open("live_data.json", "w") as f:
        json.dump(history[-50:], f, indent=2)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
