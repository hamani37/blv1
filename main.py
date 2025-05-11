from flask import Flask, request
from ml_model import process_signal

app = Flask(__name__)

@app.route('/')
def index():
    return 'Serveur IA Scalping actif.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return 'Aucune donnée reçue', 400

    response = process_signal(data)
    return response, 200
