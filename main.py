from flask import Flask, request
from ml_model import analyser_avec_openai, charger_compteur, sauvegarder_compteur
import os

app = Flask(__name__)
compteur_apprentissage = charger_compteur()

@app.route('/')
def index():
    return "🚀 Serveur IA Trading en ligne"

@app.route('/webhook', methods=['POST'])
def webhook():
    global compteur_apprentissage

    data = request.json
    if not data or 'type' not in data:
        return {"error": "Signal invalide"}, 400

    print(f"✅ Signal reçu : {data}")

    if compteur_apprentissage < 50:
        compteur_apprentissage += 1
        sauvegarder_compteur(compteur_apprentissage)
        print(f"📚 Apprentissage en cours : {compteur_apprentissage}/50")
        return {"message": f"Apprentissage {compteur_apprentissage}/50 enregistré."}, 200
    else:
        jugement, explication = analyser_avec_openai(data)
        print(f"📊 Jugement IA : {jugement.upper()} ➤ {explication}")
        return {
            "result": jugement,
            "explication": explication
        }, 200

if __name__ == '__main__':
    print("💥 Serveur Flask démarré.")
    app.run(debug=True)
