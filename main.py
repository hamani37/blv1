from flask import Flask, request
from utils.ml_model import IA_Analyser, compteur_apprentissage, sauvegarder_compteur
import os
import json

app = Flask(__name__)
ia = IA_Analyser()

@app.route("/", methods=["GET"])
def index():
    return "Serveur IA de trading actif."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    signal_type = data.get("type")
    print(f"✅ Signal reçu : {data}")

    # Apprentissage sur les 50 premiers
    if compteur_apprentissage["nb"] < 50:
        ia.train(signal_type)
        compteur_apprentissage["nb"] += 1
        sauvegarder_compteur()
        print(f"📚 Apprentissage en cours : {compteur_apprentissage['nb']}/50")
        return "Signal utilisé pour apprentissage"

    # Analyse par l'IA
    result, explication = ia.analyse(signal_type)
    print(f"📊 Explication IA : {explication}")
    return json.dumps({"result": result, "explication": explication})

if __name__ == "__main__":
    app.run(debug=True)
