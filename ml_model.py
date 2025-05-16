import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
historique = []

def apprendre_ia(data):
    global historique
    historique = data[-50:]

def prediction_ia(signal, prix, indicateurs):
    try:
        prompt = f"""
Tu es un expert en trading crypto. Analyse ce signal :
Signal : {signal.upper()}
Prix : {prix}
RSI : {indicateurs['RSI']}
MACD : {indicateurs['MACD']}
Bollinger : {indicateurs['BOLL']}
OBV : {indicateurs['OBV']}

Donne une réponse claire : ce signal est-il 🔥 bon ou 💩 mauvais ? Dis-moi pourquoi en une phrase.
        """
        reponse = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return reponse.choices[0].message["content"]
    except Exception as e:
        return f"Erreur IA: {e}"
