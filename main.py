from flask import Flask, request
import json
from datetime import datetime
from analyze_indicators import get_indicators
from openai import OpenAI
import pandas as pd
import os

app = Flask(__name__)
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

live_data_path = "live_data.json"
if not os.path.exists(live_data_path):
    with open(live_data_path, "w") as f:
        json.dump([], f)

def load_live_data():
    with open(live_data_path, "r") as f:
        return json.load(f)

def save_live_data(data):
    with open(live_data_path, "w") as f:
        json.dump(data, f, indent=2)

def variation_since_last(df, last_price):
    current_price = df['close'].iloc[-1]
    return round((current_price - last_price) / last_price * 100, 4)

def build_dataframe(data):
    return pd.DataFrame(data)[['timestamp', 'open', 'high', 'low', 'close', 'volume']].astype({
        'open': float, 'high': float, 'low': float, 'close': float, 'volume': float
    })

def generate_ia_explanation(indicators, signal_type, variation):
    prompt = f"""Tu es un expert en trading. Voici des indicateurs : {indicators}. 
Un signal {signal_type} vient d'être reçu. La variation depuis le dernier signal est de {variation} %. 
Analyse la situation avec sérieux et explique pourquoi ce signal est bon ou mauvais. Sois clair, professionnel et simple."""

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    signal_type = data.get("signal", "").upper()
    price = float(data.get("price"))
    timestamp = datetime.utcnow().isoformat()

    live_data = load_live_data()

    new_point = {
        "timestamp": timestamp,
        "open": price,
        "high": price,
        "low": price,
        "close": price,
        "volume": 1000  # valeur fictive, tu peux l'adapter
    }

    live_data.append(new_point)
    if len(live_data) > 1000:
        live_data = live_data[-1000:]
    save_live_data(live_data)

    df = build_dataframe(live_data)

    # Calcul des indicateurs
    indicators = get_indicators(df)

    # Calcul variation
    last_signal_data = next((x for x in reversed(live_data[:-1]) if "signal_type" in x), None)
    variation = 0
    if last_signal_data:
        variation = variation_since_last(df, last_signal_data["close"])

    # Filtrage : règle 0.5 %
    valid = (signal_type == "LONG" and variation > 0.5) or (signal_type == "SHORT" and variation < -0.5)

    # Explication IA
    ia_reason = generate_ia_explanation(indicators, signal_type, variation) if valid else "Signal ignoré : variation insuffisante."

    # Sauvegarde complète
    live_data[-1]["signal_type"] = signal_type
    live_data[-1]["variation"] = variation
    live_data[-1]["indicators"] = indicators
    live_data[-1]["ia_reason"] = ia_reason
    save_live_data(live_data)

    return {
        "status": "ok",
        "variation": variation,
        "valid_signal": valid,
        "ia_reason": ia_reason
    }

@app.route("/", methods=["GET"])
def root():
    return "Bot de trading IA - BLV Car"
