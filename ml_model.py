# ml_model.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def expliquer_signal(signal: str, donnees: dict, decision: bool) -> str:
    try:
        prompt = (
            f"Voici un signal de trading reçu : {signal.upper()}. "
            f"Les indicateurs sont : {donnees}. "
            f"Selon l'IA, ce signal est considéré comme {'bon' if decision else 'mauvais'}. "
            f"Explique en une phrase simple pourquoi ce signal est jugé ainsi."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # ✅ on remplace gpt-4 ici
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Erreur OpenAI : {e}"
