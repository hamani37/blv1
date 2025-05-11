import openai
import os
import json

CHEMIN_COMPTEUR = "compteur.json"

openai.api_key = os.getenv("OPENAI_API_KEY")  # clé stockée dans Render

def charger_compteur():
    if os.path.exists(CHEMIN_COMPTEUR):
        with open(CHEMIN_COMPTEUR, 'r') as f:
            return json.load(f).get("valeur", 0)
    return 0

def sauvegarder_compteur(valeur):
    with open(CHEMIN_COMPTEUR, 'w') as f:
        json.dump({"valeur": valeur}, f)

def analyser_avec_openai(signal):
    try:
        message_systeme = (
            "Tu es une IA experte en trading crypto. "
            "Quand on te donne un signal (type 'long' ou 'short'), tu dis si c'est un bon ou mauvais signal. "
            "Et tu expliques ton raisonnement de façon marrante ou vulgaire, comme un trader qui a du caractère. "
            "Sois direct, franc, et drôle si possible."
        )

        message_utilisateur = f"Voici le signal reçu : {signal}. Ce signal est-il bon ou mauvais ? Explique avec ton style."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": message_systeme},
                {"role": "user", "content": message_utilisateur}
            ],
            temperature=0.9
        )

        reponse = response.choices[0].message.content.strip()
        if "mauvais" in reponse.lower():
            return "mauvais", reponse
        else:
            return "bon", reponse

    except Exception as e:
        return "erreur", f"Erreur IA OpenAI : {str(e)}"
