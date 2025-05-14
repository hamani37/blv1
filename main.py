from flask import Flask, request, jsonify
from utils.ml_model import analyser_signal
from utils.indicateurs import recuperer_prix_binance_et_indicateurs
from utils.logbook import enregistrer_log
import os
import json

app = Flask(__name__)

DATA_FILE = "data/live_data.json"
APPRENTISSAGE_MAX = 50

# Chargement des données existantes
if not os.path.exists("data"):
    os.makedirs("data")

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {
        "historique": [],
        "compteur_apprentissage": 0,
        "dernier_signal": None
    }

@app.route("/", methods=["GET"])
def home():
    return "✅ Serveur IA Trading OPÉRATIONNEL ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    signal = request.json
    print(f"✅ Signal reçu : {signal}")

    # Récupération prix et indicateurs Binance
    info_marche = recuperer_prix_binance_et_indicateurs(signal["type"])
    if info_marche is None:
        return jsonify({"error": "Impossible de récupérer les données du marché"}), 500

    # Entraînement si pas encore terminé
    if data["compteur_apprentissage"] < APPRENTISSAGE_MAX:
        data["compteur_apprentissage"] += 1
        print(f"📚 Apprentissage en cours : {data['compteur_apprentissage']}/{APPRENTISSAGE_MAX}")
        phase = "Phase d'apprentissage"
    else:
        phase = "Analyse IA"

    # Analyse du signal par IA
    interpretation = analyser_signal(signal, info_marche, phase)

    # Log stylé avec tout ce qu’il faut
    enregistrer_log(signal, info_marche, interpretation, phase)

    # Sauvegarde de l’état
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
