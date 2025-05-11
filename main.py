import os
from flask import Flask, request, jsonify
from datetime import datetime
import logging
import json

app = Flask(__name__)

# Configuration des logs
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Chargement de la clé API OpenAI depuis les variables d'environnement (si nécessaire plus tard)
openai_api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def index():
    return "Serveur IA - Webhook actif !"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if not data or 'type' not in data:
            logging.warning("❌ Données invalides reçues.")
            return jsonify({"error": "Invalid data"}), 400

        signal_type = data['type']
        logging.info(f"✅ Signal reçu : {data}")
        print(f"✅ Signal reçu : {data}")

        # Ici tu peux ajouter le traitement IA avec ton modèle ML ou OpenAI selon les prochaines étapes

        return jsonify({"status": "Signal reçu", "type": signal_type}), 200
    except Exception as e:
        logging.error(f"❌ Erreur dans le webhook : {str(e)}")
        return jsonify({"error": "Erreur serveur"}), 500
