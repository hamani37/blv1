import os
import json
import time
import threading
import requests
from flask import Flask, request, jsonify
from ml_model import IA_Pro

app = Flask(__name__)
model = IA_Pro()

SIGNAL_FILE = "data/signals.json"
PRICE_FILE = "data/price_history.json"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_current_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
        response = requests.get(url)
        return response.json()["solana"]["usd"]
    except:
        return None

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f)

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def log_colored(msg, color="blue"):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "end": "\033[0m"
    }
    print(f"{colors[color]}{msg}{colors['end']}")

@app.route("/", methods=["GET"])
def index():
    return "IA Scalping Render OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    signal = request.get_json()
    signal_type = signal.get("type", "unknown")
    price = get_current_price()
    if price is None:
        return jsonify({"error": "Prix introuvable"}), 500

    log_colored(f"✅ Signal reçu : {signal}", "green")
    
    if model.apprentissage_en_cours():
        model.entrainer(signal, price)
        log_colored(f"📚 Apprentissage en cours : {model.get_compteur()}/50", "yellow")
    else:
        decision, explication = model.analyser(signal, price)
        log_colored(f"📊 IA a jugé ce signal comme : {decision.upper()}", "blue")
        log_colored(f"📢 Explication : {explication}", "green")

    # Enregistrement historique
    historique = load_json(SIGNAL_FILE)
    historique.append({"signal": signal_type, "prix": price, "timestamp": time.time()})
    save_json(historique, SIGNAL_FILE)

    return jsonify({"status": "ok"})

def suivi_price():
    while True:
        prix = get_current_price()
        if prix:
            log_colored(f"[SUIVI] Prix actuel : {prix} $", "yellow")
            historique = load_json(PRICE_FILE)
            historique.append({"timestamp": time.time(), "prix": prix})
            save_json(historique[-300:], PRICE_FILE)
        time.sleep(1)

if __name__ == "__main__":
    log_colored("[BOOT] Démarrage serveur IA...", "blue")
    threading.Thread(target=suivi_price, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
