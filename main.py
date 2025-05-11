# main.py

from flask import Flask, request, jsonify
from ml_model import expliquer_signal
import time

app = Flask(__name__)

# Stockage des signaux pour analyse entre deux
signaux_reçus = []

@app.route('/')
def home():
    return "🔗 Serveur IA actif et prêt à recevoir des signaux."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"✅ Signal reçu : {data}")

    type_signal = data.get("type")
    timestamp = time.time()

    # Ajouter ce signal dans l'historique
    signaux_reçus.append({
        "type": type_signal,
        "timestamp": timestamp,
        "prix": get_mock_price()  # Remplace par le vrai prix via API externe plus tard
    })

    decision = True  # Pour le moment on considère le signal comme "bon"

    # Si on a au moins deux signaux, on analyse
    if len(signaux_reçus) >= 2:
        prev = signaux_reçus[-2]
        curr = signaux_reçus[-1]

        variation = (
            ((curr["prix"] - prev["prix"]) / prev["prix"]) * 100
            if prev["type"] == "long"
            else ((prev["prix"] - curr["prix"]) / prev["prix"]) * 100
        )

        decision = variation >= 0.5

    # Simuler les indicateurs (remplacer par de vrais calculs plus tard)
    indicateurs = {
        "RSI": 61.5,
        "MACD": -0.3,
        "Volume": 489321,
        "Trend": "haussière",
        "Support": 24500,
        "Resistance": 25200
    }

    message = expliquer_signal(
        signal=type_signal,
        donnees=indicateurs,
        decision=decision
    )

    print(f"📊 Explication IA : {message}")

    return jsonify({
        "statut": "OK",
        "signal": type_signal,
        "decision": "bon" if decision else "mauvais",
        "explication": message
    })

def get_mock_price():
    # 🧪 Simule un prix aléatoire pour les tests
    import random
    return round(random.uniform(100, 200), 2)

if __name__ == '__main__':
    app.run(debug=True)
