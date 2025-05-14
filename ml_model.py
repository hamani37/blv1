import openai
import os
import requests
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
        response = requests.get(url).json()
        return float(response['price'])
    except Exception as e:
        return None

def get_indicators():
    # Simulation réaliste d'indicateurs, à remplacer plus tard par vrais calculs si besoin
    return {
        "RSI": round(random.uniform(40, 80), 2),
        "MACD": round(random.uniform(-2, 2), 2),
        "Boll": round(random.uniform(0.5, 2.5), 2),
        "OBV": round(random.uniform(1000, 10000), 2),
    }

def analyser_signal(signal_type):
    prix = get_price()
    indicateurs = get_indicators()

    if not prix:
        return "❌ Erreur de récupération du prix."

    message = f"📈 Signal: {signal_type.upper()} | Prix: {prix} | RSI: {indicateurs['RSI']} | MACD: {indicateurs['MACD']} | Boll: {indicateurs['Boll']} | OBV: {indicateurs['OBV']}\nPhase d'apprentissage"

    try:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en crypto. Rends les analyses claires et sérieuses."},
                {"role": "user", "content": f"Voici un signal {signal_type} avec un prix de {prix} USDT. Indicateurs: {indicateurs}. Donne une analyse simple et claire."}
            ]
        )
        interpretation = completion.choices[0].message.content.strip()
        return f"{message}\n🧠 Réponse IA:\n{interpretation}"
    except Exception as e:
        return f"{message}\nErreur IA: \n{str(e)}"
