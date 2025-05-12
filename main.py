from flask import Flask, request, jsonify
from ml_model import process_signal
import threading
import time
import json
import os

app = Flask(__name__)

# Globals
data_file = "data/live_data.json"
latest_price = None
price_history = []
training_counter = 0
max_training = 50
last_signal_time = None
last_signal_type = None
last_signal_price = None

# Chargement de l'état précédent
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        saved = json.load(f)
        training_counter = saved.get("training_counter", 0)
        last_signal_type = saved.get("last_signal_type")
        last_signal_price = saved.get("last_signal_price")
        last_signal_time = saved.get("last_signal_time")

@app.route("/")
def index():
    return "Serveur IA opérationnel"

@app.route("/webhook", methods=["POST"])
def webhook():
    global training_counter, last_signal_time, last_signal_type, last_signal_price, price_history
    signal = request.json
    print(f"✅ Signal reçu : {signal}")

    if last_signal_price is not None:
        variations = [abs(p - last_signal_price) / last_signal_price * 100 for p in price_history]
        max_variation = max(variations) if variations else 0
        variation_direction = max(price_history) - last_signal_price if last_signal_type == "long" else last_signal_price - min(price_history)
        variation_percent = (variation_direction / last_signal_price) * 100
        is_good = variation_percent >= 0.5

        log = {
            "signal": last_signal_type,
            "start_price": last_signal_price,
            "max_price": max(price_history),
            "min_price": min(price_history),
            "end_price": price_history[-1],
            "variation_percent": round(variation_percent, 4),
            "is_good": is_good,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print("\n\033[92m[VARIATION LOG]\033[0m", json.dumps(log, indent=2), "\n")

    # Reset pour le nouveau signal
    last_signal_time = time.time()
    last_signal_type = signal["type"]
    last_signal_price = latest_price
    price_history = []

    # Phase d'apprentissage
    if training_counter < max_training:
        training_counter += 1
        print(f"\033[94m📚 Apprentissage en cours : {training_counter}/{max_training}\033[0m")
    else:
        judgment = process_signal(signal, latest_price)
        print(f"\033[93m📊 Jugement IA : {judgment}\033[0m")

    # Sauvegarde
    with open(data_file, "w") as f:
        json.dump({
            "training_counter": training_counter,
            "last_signal_type": last_signal_type,
            "last_signal_price": last_signal_price,
            "last_signal_time": last_signal_time
        }, f)

    return jsonify({"status": "ok"})

# Récupération du prix en live (via CoinGecko simple API mock)
def fetch_price():
    global latest_price, price_history
    import requests
    while True:
        try:
            r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
            latest_price = r.json()["solana"]["usd"]
            if last_signal_price is not None:
                price_history.append(latest_price)
            time.sleep(1)
        except Exception as e:
            print("[Erreur récupération prix]", e)
            time.sleep(2)

if __name__ == "__main__":
    print("[BOOT] Nouveau modèle IA initialisé.")
    print(f"[BOOT] Compteur apprentissage : {training_counter}/{max_training}")
    threading.Thread(target=fetch_price, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
