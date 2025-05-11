from flask import Flask, request, jsonify
from ml_model import SignalAnalyzer
import pandas as pd
import openai
import os

app = Flask(__name__)
model = SignalAnalyzer()
signals = []

# Met ta clé API OpenAI dans les variables Render ou .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_features(data):
    # Extrait les "features" : tu dois adapter ça avec les vrais indicateurs
    return [data.get("rsi", 50), data.get("volume", 100)]  # EXEMPLE

def get_explanation(features, prediction):
    prompt = f"Le signal avec les caractéristiques {features} a été jugé comme '{prediction}'. Explique pourquoi."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("✅ Signal reçu :", data)

    signal_type = data.get("type", "unknown")
    features = extract_features(data)

    if len(signals) < 50:
        signals.append({"features": features, "label": signal_type})
        return jsonify({"status": "Signal enregistré pour apprentissage."})

    elif len(signals) == 50 and not model.trained:
        df = pd.DataFrame(signals)
        model.train(df)
        print("📊 IA entraînée avec les 50 premiers signaux.")
        return jsonify({"status": "IA entraînée. Prête à filtrer."})

    else:
        prediction = model.predict(features)
        explanation = get_explanation(features, prediction)
        print(f"🧠 Prédiction IA : {prediction}")
        print(f"🗒️ Explication : {explanation}")

        if prediction == "long":
            print("📤 Signal envoyé vers Webhennok (exemple)")

        return jsonify({
            "prediction": prediction,
            "explanation": explanation
        })

if __name__ == "__main__":
    app.run(debug=True)
