from flask import Flask, request, jsonify
import json
import os
import time
from utils.ml_model import process_signal
from utils.analyse_signal import log_analysis, update_live_price, init_background_tasks

app = Flask(__name__)

data_file = 'data/live_data.json'
signal_log_file = 'data/signal_log.json'

# ✅ Crée le dossier s'il n'existe pas
os.makedirs("data", exist_ok=True)

# Charger les signaux existants
if os.path.exists(signal_log_file):
    with open(signal_log_file, "r") as f:
        signal_log = json.load(f)
else:
    signal_log = []

# Charger les données live
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        live_data = json.load(f)
else:
    live_data = {
        "last_price": None,
        "last_signal": None,
        "variation": None
    }

# Initialisation IA
print("[BOOT] Nouveau modèle IA initialisé.")
print(f"[BOOT] Compteur apprentissage : {len(signal_log)}/50")
init_background_tasks()

@app.route('/')
def home():
    return "BLV IA Active"

@app.route('/webhook', methods=['POST'])
def webhook():
    signal = request.get_json()
    print(f"✅ Signal reçu : {signal}")

    # Analyse IA
    result = process_signal(signal, signal_log, live_data)

    # Affichage log
    log_analysis(signal, result, signal_log)

    # Enregistrement
    signal_log.append({
        "type": signal["type"],
        "judgment": result["judgment"],
        "explanation": result["explanation"],
        "price": live_data["last_price"],
        "variation": live_data["variation"],
        "timestamp": time.time()
    })

    # ✅ Sauvegarde fichiers JSON
    with open(signal_log_file, "w") as f:
        json.dump(signal_log, f, indent=2)

    with open(data_file, "w") as f:
        json.dump(live_data, f, indent=2)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
