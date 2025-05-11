from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Historique des signaux reçus pour les tests IA
history = []

@app.route('/')
def index():
    return "🧠 Webhook IA actif - Render OK"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or 'type' not in data:
        return jsonify({'error': 'Format JSON invalide ou type manquant'}), 400

    signal_type = data['type']
    timestamp = datetime.utcnow().isoformat()

    # Ajout du signal au log interne (pour analyse IA plus tard)
    history.append({
        'timestamp': timestamp,
        'type': signal_type
    })

    print(f"✅ Signal reçu : {data}")

    return jsonify({
        'status': 'reçu',
        'type': signal_type,
        'timestamp': timestamp
    }), 200
