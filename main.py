from flask import Flask, request, jsonify
from utils.analyse_signal import analyser_signal
from utils.execute_trade import executer_trade
import json
import os

app = Flask(__name__)
compteur_fichier = "signal_count.json"

# Initialiser le compteur s'il n'existe pas
if not os.path.exists(compteur_fichier):
    with open(compteur_fichier, "w") as f:
        json.dump({"count": 0}, f)

@app.route('/')
def home():
    return "🚀 Webhook de trading IA actif !"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal_type = data.get('type')

    # Charger compteur
    with open(compteur_fichier, "r") as f:
        compteur_data = json.load(f)

    compteur = compteur_data.get("count", 0)

    print(f"✅ Signal reçu : {data}")
    print(f"📊 Signal n°{compteur + 1} / 50 (phase d'apprentissage)")

    if compteur < 50:
        print("🧠 Phase d'apprentissage : enregistrement du signal...")
        analyser_signal(data, apprentissage=True)
        compteur += 1
        with open(compteur_fichier, "w") as f:
            json.dump({"count": compteur}, f)
        return jsonify({"status": "learning", "compteur": compteur})
    else:
        print("🎯 Phase IA : décision en cours...")
        resultat = analyser_signal(data, apprentissage=False)
        if resultat == "go":
            print("✅ L'IA valide ce signal, envoi à l'exécution.")
            executer_trade(data)
        else:
            print("❌ Signal ignoré par l'IA.")
        return jsonify({"status": "decision", "decision": resultat})

if __name__ == '__main__':
    app.run(debug=True)
