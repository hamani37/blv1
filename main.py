# main.py

from flask import Flask, request, jsonify
import datetime
import ml_model
import os
import openai

app = Flask(__name__)

# Configuration de l'API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Stockage temporaire du dernier signal reçu
last_signal = None

# Stockage du dernier prix connu
last_price = None

@app.route("/")
def home():
    return "🚀 Webhook IA prêt à recevoir des signaux."

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_signal, last_price

    data = request.json
    if not data or "type" not in data:
        return jsonify({"status": "error", "message": "Signal invalide"}), 400

    signal_type = data["type"]
    current_price = float(data.get("price", 0))

    # Vérifier que le prix est fourni
    if current_price == 0:
        return jsonify({"status": "error", "message": "Prix manquant"}), 400

    print(f"✅ Signal reçu : {data}")

    # Enregistrement du dernier signal et du prix
    now = datetime.datetime.utcnow().isoformat()
    features = {
        "type": 1 if signal_type == "long" else 0,
        "price": current_price,
        "timestamp": now,
        "rsi": float(data.get("rsi", 0)),
        "volume": float(data.get("volume", 0)),
        "macd": float(data.get("macd", 0)),
        "atr": float(data.get("atr", 0)),
        "valid": None  # À définir après évaluation
    }

    # Cas 1 : apprentissage (50 premiers signaux)
    signal_history = ml_model.load_signal_history()
    if len(signal_history) < 50:
        # Pas de validation, on stocke pour entraînement plus tard
        features["valid"] = check_profit_logic(signal_type, current_price)
        ml_model.add_signal_to_history(features)
        ml_model.train_model()
        log = generate_explanation(features, features["valid"])
        return jsonify({"status": "ok", "phase": "training", "log": log})

    # Cas 2 : IA juge le signal
    is_valid = ml_model.evaluate_signal(features)
    features["valid"] = is_valid
    ml_model.add_signal_to_history(features)

    if is_valid:
        log = generate_explanation(features, True)
        # Exemple d’envoi webhook ici si valide
        print("📡 SIGNAL VALIDE – envoyer vers Webhennok")
    else:
        log = generate_explanation(features, False)

    return jsonify({"status": "ok", "valid": is_valid, "log": log})


def check_profit_logic(signal_type, price):
    global last_signal, last_price
    if not last_signal or not last_price:
        last_signal = signal_type
        last_price = price
        return False

    if last_signal == "long":
        if price >= last_price * 1.005:
            result = True
        else:
            result = False
    elif last_signal == "short":
        if price <= last_price * 0.995:
            result = True
        else:
            result = False
    else:
        result = False

    last_signal = signal_type
    last_price = price
    return result


def generate_explanation(features, valid):
    explanation = f"🧠 Signal {'valide ✅' if valid else 'invalide ❌'} avec les paramètres :\n"
    for key, value in features.items():
        if key != "valid":
            explanation += f"- {key} : {value}\n"
    if openai.api_key:
        try:
            prompt = f"Explique pourquoi ce signal {'est bon' if valid else 'est mauvais'} : {features}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un assistant de trading qui analyse des signaux techniques."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            explanation += "\n🤖 OpenAI : " + response["choices"][0]["message"]["content"]
        except Exception as e:
            explanation += f"\n⚠️ Erreur OpenAI : {str(e)}"
    return explanation
