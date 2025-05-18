from flask import Flask, request, jsonify
import openai
import os
from datetime import datetime
from get_price import get_price_data
from analyze_indicators import get_indicators
from log_utils import log_signal, save_signal_to_json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

last_signal_time = None
last_price = None

@app.route("/", methods=["GET"])
def home():
    return "Bot IA de trading – BLV Car 🧠💰"

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_signal_time, last_price

    data = request.get_json()
    print("📩 Signal reçu:", data)

    symbol = data.get("symbol")
    interval = data.get("interval")

    if not symbol or not interval:
        return jsonify({"error": "Paramètres symbol ou interval manquants"}), 400

    price_data = get_price_data(symbol, interval)
    if price_data is None:
        return jsonify({"error": "Impossible d’obtenir les données de prix"}), 500

    indicators = get_indicators(price_data)
    if indicators is None:
        return jsonify({"error": "Erreur dans le calcul des indicateurs"}), 500

    current_price = price_data["close"].iloc[-1]
    signal_time = datetime.utcnow().isoformat()

    variation = None
    if last_price is not None:
        variation = ((current_price - last_price) / last_price) * 100

    last_price = current_price
    last_signal_time = signal_time

    messages = [
        {"role": "system", "content": "Tu es un expert en trading crypto. Tu donnes des analyses claires et sérieuses."},
        {"role": "user", "content": f"""Voici les indicateurs pour {symbol} :
- Prix actuel : {current_price:.4f} $
- RSI : {indicators['RSI']}
- MACD : {indicators['MACD']}
- Signal MACD : {indicators['MACD_SIGNAL']}
- Bollinger haut : {indicators['BOLLINGER_HIGH']}
- Bollinger bas : {indicators['BOLLINGER_LOW']}
- OBV : {indicators['OBV']}
- VWAP : {indicators['VWAP']}
- ATR : {indicators['ATR']}
- SuperTrend : {indicators['SUPERTREND']}
- Variation depuis le dernier signal : {variation:.2f}%\n

Donne un avis sur le marché (LONG / SHORT / AUCUN), avec une explication sérieuse."""}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

        ai_response = response.choices[0].message["content"].strip()
        print("🧠 Réponse de l'IA :", ai_response)

        log_signal(symbol, interval, current_price, variation, ai_response)
        save_signal_to_json(symbol, interval, current_price, variation, ai_response)

        return jsonify({
            "message": "Signal reçu et analysé.",
            "price": current_price,
            "variation": variation,
            "ia_response": ai_response
        })

    except Exception as e:
        print("Erreur IA:", e)
        return jsonify({"error": "Erreur lors de l’appel à l’IA."}), 500

if __name__ == "__main__":
    app.run(debug=True)
