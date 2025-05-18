from flask import Flask, request, jsonify
import openai
import os
import sys
from datetime import datetime
from get_price import get_price_data
from analyze_indicators import get_indicators
from log_utils import log_signal, save_signal_to_json

# Configuration pour Render
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "SOL/USD 1M Trading Bot - BLV Car 🔥"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("📩 Signal reçu:", data)

        # Paramètres fixes pour SOL/USD 1min
        symbol = "SOLUSDT"
        interval = "1m"

        price_data = get_price_data(symbol, interval)
        if price_data is None or price_data.empty:
            return jsonify({"error": "Données prix indisponibles"}), 500

        indicators = get_indicators(price_data)
        if not indicators:
            return jsonify({"error": "Erreur indicateurs"}), 500

        current_price = price_data["close"].iloc[-1]

        # Vérification des clés des indicateurs
        required_keys = ['rsi', 'macd', 'macd_signal', 'bollinger_high', 'bollinger_low']
        if not all(key in indicators for key in required_keys):
            return jsonify({"error": "Indicateurs incomplets"}), 500

        # Construction du message pour GPT
        messages = [
            {"role": "system", "content": "Expert trading SOL/USD 1min."},
            {"role": "user", "content": f"""Données SOL/USD:
- Prix: {current_price:.4f}$
- RSI: {indicators['rsi']}
- MACD: {indicators['macd']:.5f}
- Bollinger: {indicators['bollinger_high']:.5f}|{indicators['bollinger_low']:.5f}
- Volume: {indicators['obv']:.2f}
Analyse en 2 lignes. Réponse formatée: [DIRECTION] [CONFIDENCE%] [RAISON]"""}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.3,
            max_tokens=100
        )

        ai_response = response.choices[0].message["content"].strip()
        print("🧠 Réponse IA:", ai_response)

        # Log et sauvegarde
        log_signal(symbol, interval, current_price, None, ai_response)
        save_signal_to_json(symbol, interval, current_price, None, ai_response)

        return jsonify({
            "status": "success",
            "analysis": ai_response,
            "price": current_price
        })

    except Exception as e:
        print(f"🚨 Erreur globale: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
