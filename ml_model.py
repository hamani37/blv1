import openai
import os
import json
from log_utils import get_last_price_variation

openai.api_key = os.getenv("OPENAI_API_KEY")

def ia_analyse_signal(signal, price, indicators):
    try:
        variation = get_last_price_variation(price)

        instruction = f"""
Tu es une IA de trading sérieuse et stricte.
Voici les données techniques :
- Signal reçu : {signal}
- Variation entre les deux derniers signaux : {variation:.2f}%
- Indicateurs : {json.dumps(indicators, indent=2)}

Règles à respecter :
- VALIDE un signal LONG uniquement si variation >= +0.5 %
- VALIDE un signal SHORT uniquement si variation <= -0.5 %
- Sinon, REFUSE de valider le signal.

Réponds uniquement par 'VALIDE' ou 'REFUSE', suivi d'une explication sérieuse et concise.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": instruction}],
            temperature=0.4
        )

        reply = response['choices'][0]['message']['content']
        decision = "VALIDE" if "VALIDE" in reply.upper() else "REFUSE"

        return decision, reply.strip()

    except Exception as e:
        return "REFUSE", f"Erreur IA : {str(e)}"
