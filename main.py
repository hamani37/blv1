from flask import Flask, request
from datetime import datetime
import json
import os
from utils.decision import should_trade
from utils.execute_trade import execute_trade
from utils.analyse_signal import analyse_signal

app = Flask(__name__)

SIGNAL_LOG_PATH = "data/signal_count.json"

def init_signal_log():
    today = datetime.utcnow().date().isoformat()
    if not os.path.exists(SIGNAL_LOG_PATH):
        os.makedirs(os.path.dirname(SIGNAL_LOG_PATH), exist_ok=True)
        with open(SIGNAL_LOG_PATH, "w") as f:
            json.dump({"date": today, "count": 0}, f)

def get_signal_count():
    with open(SIGNAL_LOG_PATH, "r") as f:
        data = json.load(f)
    return data

def increment_signal_count():
    today = datetime.utcnow().date().isoformat()
    data = get_signal_count()
    if data["date"] != today:
        data = {"date": today, "count": 1}
    else:
        data["count"] += 1
    with open(SIGNAL_LOG_PATH, "w") as f:
        json.dump(data, f)
    return data["count"]

@app.route('/')
def home():
    return "Serveur IA de Trading actif."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    signal_type = data.get("type", "")
    signal_number = increment_signal_count()

    print(f"✅ Signal reçu : {data}")
    print(f"🧠 Apprentissage : {signal_number} / 50 signaux collectés")

    if signal_number <= 50:
        print("📊 Mode apprentissage : ce signal est stocké uniquement pour entraînement.")
        analyse_signal(data, mode="training")
        return {"status": "learning", "received": True}

    # Sinon, prise de décision IA + trade
    if should_trade(data):
        result = execute_trade(data)
        return {"status": "executed", "result": result}
    else:
        return {"status": "ignored", "reason": "IA rejeté ce signal"}

if __name__ == '__main__':
    init_signal_log()
    app.run(host='0.0.0.0', port=10000)
