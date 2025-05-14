from flask import Flask, request
from ml_model import analyser_signal
from log_utils import log_color
import os

app = Flask(__name__)

signal_counter = 0

@app.route('/')
def home():
    return "🚀 Serveur IA Trading en ligne."

@app.route('/webhook', methods=['POST'])
def webhook():
    global signal_counter
    data = request.get_json()
    signal_type = data.get("type", "").lower()

    if signal_type in ["long", "short"]:
        signal_counter += 1
        print(f"✅ Signal reçu : {data}")
        print(f"📚 Apprentissage en cours : {signal_counter}/50")
        interpretation = analyser_signal(signal_type)
        log_color(interpretation)
        return "Signal traité", 200
    else:
        return "Signal non reconnu", 400

if __name__ == "__main__":
    app.run(debug=True)
