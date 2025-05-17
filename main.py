from flask import Flask, request, jsonify
from log_utils import log_message
from ml_model import analyze_signal_with_ai
from indicators import fetch_price_and_indicators
import json
import time

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    log_message(f"✅ Nouveau signal reçu : {data}")

    try:
        live_data = fetch_price_and_indicators()
        log_message(f"📊 Données récupérées : {live_data}")
    except Exception as e:
        log_message(f"❌ Erreur lors de la récupération des données en direct : {e}")
        return jsonify({'status': 'error', 'message': str(e)})

    try:
        decision, explanation = analyze_signal_with_ai(data, live_data)
        log_message(f"🤖 IA : {explanation}")

        # Sauvegarde dans le fichier
        with open("live_data.json", "a") as f:
            f.write(json.dumps({
                "timestamp": time.time(),
                "signal": data,
                "live_data": live_data,
                "decision": decision,
                "explanation": explanation
            }) + "\n")

        return jsonify({'status': 'success', 'decision': decision, 'explanation': explanation})
    except Exception as e:
        log_message(f"❌ Erreur dans l'analyse IA : {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/')
def index():
    return "🟢 Serveur IA de Trading en ligne"

if __name__ == '__main__':
    app.run(debug=True)
