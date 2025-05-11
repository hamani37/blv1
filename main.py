from flask import Flask, request, jsonify
import os
import json
import openai
from datetime import datetime

app = Flask(__name__)

# Clé API OpenAI depuis le fichier .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Log des signaux
SIGNAL_LOG_FILE = "logs/signals.jsonl"
os.makedirs("logs", exist_ok=True)

# Enregistrer un signal dans un fichier
def log_signal(signal_data):
    signal_data["timestamp"] = datetime.utcnow().isoformat()
    with open(SIGNAL_LOG_FILE, "a") as f:
        f.write(json.dumps(signal_data) + "\n")

# Appel à l’API OpenAI pour expliquer un signal
def explain_signal(signal_type, indicators, result):
    prompt = f"""
Tu es une IA d’analyse de signaux de trading.
Tu dois expliquer pourquoi un signal est {result.upper()}.

Signal reçu : {signal_type}
Indicateurs disponibles :
{json.dumps(indicators, indent=2)}

Explique de façon claire et concise, en une phrase ou deux maximum.
"""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en stratégie de trading algorithmique."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return completion.choices[0].message["content"].strip()
    except Exception as e:
        return f"Erreur OpenAI : {e}"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data or "type" not in data:
        return jsonify({"status": "error", "message": "Signal invalide"}), 400

    signal_type = data["type"]
    indicators = data.get("indicators", {})  # ex: { "rsi": 55, "volume": 932000 }
    result = data.get("result", "inconnu")  # temporairement en mode test

    log_signal({
        "type": signal_type,
        "indicators": indicators,
        "result": result
    })

    explication = explain_signal(signal_type, indicators, result)

    print("✅ Signal reçu :", data)
    print("📊 Explication IA :", explication)

    return jsonify({"status": "ok", "explication": explication})

@app.route("/", methods=["GET"])
def home():
    return "🚀 Serveur IA Trading prêt à recevoir des signaux."
