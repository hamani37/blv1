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

if os.getenv("RENDER_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

last_signal_time = None
last_price = None

@app.route("/", methods=["GET"])
def home():
    return "SOL/USD 1M Trading Bot - BLV Car 🔥"

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_signal_time, last_price

    data = request.get_json()
    print("📩 Signal reçu:", data)

    # Paramètres fixes pour SOL/USD 1min
    symbol = "SOLUSDT"  # Forcé à SOL/USD
    interval = "1m"     # Forcé à 1 minute

    price_data = get_price_data(symbol, interval)
    if price_data is None:
        return jsonify({"error": "Données SOL/USD non disponibles"}), 500

    indicators = get_indicators(price_data)
    if indicators is None:
        return jsonify({"error": "Erreur indicateurs SOL/USD"}), 500

    current_price = price_data["close"].iloc[-1]
    signal_time = datetime.utcnow().isoformat()

    variation = None
    if last_price is not None:
        variation = ((current_price - last_price) / last_price) * 100

    last_price = current_price
    last_signal_time = signal_time

    messages = [
        {"role": "system", "content": "Expert trading SOL/USD en timeframe 1 minute."},
        {"role": "user", "content": f"""Données SOL/USD 1min :
- Prix actuel : {current_price:.4f} $
- RSI (14) : {indicators['RSI']}
- MACD : {indicators['MACD']:.5f} / Signal : {indicators['MACD_SIGNAL']:.5f}
- Bollinger : {indicators['BOLLINGER_HIGH']:.5f} | {indicators['BOLLINGER_LOW']:.5f}
- Volume (OBV) : {indicators['OBV']:.2f}
- ATR (14) : {indicators['ATR']:.5f}
- SuperTrend : {'🟢 LONG' if indicators['SUPERTREND'] else '🔴 SHORT'}
- Variation depuis dernier signal : {variation:.2f}%

Analyse précise en 3 lignes max. Réponse formatée : [DIRECTION] [CONFIDENCE%] [EXPLICATION]"""}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150,
            temperature=0.3
        )

        ai_response = response.choices[0].message["content"].strip()
        print("🧠 Réponse IA SOL/USD:", ai_response)

        log_signal(symbol, interval, current_price, variation, ai_response)
        save_signal_to_json(symbol, interval, current_price, variation, ai_response)

        return jsonify({
            "message": "Signal SOL/USD traité",
            "price": current_price,
            "variation": f"{variation:.2f}%" if variation else None,
            "analysis": ai_response
        })

    except Exception as e:
        print("Erreur IA SOL/USD:", e)
        return jsonify({"error": "Erreur analyse SOL/USD"}), 500

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
