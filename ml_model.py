import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_signal(signal_type, indicators):
    try:
        prompt = f"""
Tu es un expert en trading crypto. Analyse ce signal de type {signal_type.upper()} reçu avec ces indicateurs :
Prix actuel : {indicators['last']} USD
Variation max : {indicators['high']} USD
Variation min : {indicators['low']} USD
RSI : {indicators['rsi']}
MACD : {indicators['macd']}
Bollinger : {indicators['boll']}
OBV : {indicators['obv']}

Donne un avis très clair et court (sans blague ni humour).
"""
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"Erreur IA: {str(e)}"
