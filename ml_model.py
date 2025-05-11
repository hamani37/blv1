# ml-model.py

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def expliquer_signal(signal, donnees, decision):
    try:
        prompt = (
            f"Tu es un expert en analyse de signaux de trading. "
            f"Tu dois expliquer si le signal reçu est bon ou mauvais en te basant sur les indicateurs suivants :\n"
            f"{donnees}\n\n"
            f"Le signal était de type : {signal}.\n"
            f"L'IA a décidé que ce signal était : {'✅ bon' if decision else '❌ mauvais'}.\n"
            f"Explique pourquoi."
        )

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en trading crypto."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Erreur OpenAI : {e}"
