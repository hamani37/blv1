from flask import Flask, request
from ml_model import apprendre_ia, prediction_ia
from log_utils import log_message
from indicateurs import get_all_indicators
import requests
import json
import os
import time

app = Flask(__name__)

data_file = "live_data.json"
API_BINANCE = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"

historique_signaux = []
previous_price = None

def get_live_price():
    try:
        response = requests.get(API_BINANCE)
        return float(response.json()["price"])
    except:
        return None

@app.route("/webhook", methods=["POST"])
def webhook():
    global previous_price

    data = request.json
    signal = data.get("type")

    if signal not in ["long", "short"]:
        return "Signal invalide", 400

    prix = get_live_price()
    indicateurs = get_all_indicators()
    message = f"📈 Signal: {signal.upper()} | Prix: {prix} | RSI: {indicateurs['RSI']} | MACD: {indicateurs['MACD']} | Boll: {indicateurs['BOLL']} | OBV: {indicateurs['OBV']}"

    variation_max = None
    variation_min = None
    if previous_price is not None and prix is not None:
        variation = prix - previous_price
        variation_max = max(prix, previous_price)
        variation_min = min(prix, previous_price)
        message += f"\n🟡 Variation max : {variation_max} | Variation min : {variation_min}"

    print(message)
    log_message(message)

    historique_signaux.append({"signal": signal, "prix": prix, "indicateurs": indicateurs})

    if len(historique_signaux) < 50:
        print(f"📚 Apprentissage en cours : {len(historique_signaux)}/50\nPhase d'apprentissage")
        apprendre_ia(historique_signaux)
    else:
        prediction = prediction_ia(signal, prix, indicateurs)
        print(f"🤖 IA : {prediction}")

    previous_price = prix
    try:
        with open(data_file, "w") as f:
            json.dump(historique_signaux, f)
    except:
        pass

    return "Signal reçu", 200

@app.route("/")
def home():
    return "Serveur actif."

if __name__ == "__main__":
    app.run(debug=True)
