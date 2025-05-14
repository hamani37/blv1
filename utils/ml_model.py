# utils/ml_model.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyser_signal(signal, info_marche, phase):
    prompt = f"""
Tu es un analyste crypto professionnel.
Voici un nouveau signal reçu : {signal}
Voici les données du marché :
- Prix actuel : {info_marche['price']}
- RSI : {info_marche['rsi']}
- MACD : {info_marche['macd']}
- Bollinger : {info_marche['bollinger']}
- OBV : {info_marche['obv']}

Phase : {phase}

Donne ton avis comme un expert, avec un langage un peu marrant et une touche vulgaire. Conclue par : 
- ✅ Bon signal 
ou 
- ❌ Signal pourri

Sois clair et direct.
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en crypto-trading avec un langage franc et drôle."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"Erreur IA: {e}"
