from flask import Flask, request, jsonify
import openai
import os
import sys
import requests
from datetime import datetime
from get_price import RealTimeData
from analyze_indicators import calculate_indicators
from ml_model import TradingAIAutoLearn
from log_utils import save_trading_log
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
WEBHOOK_TARGET = os.getenv("TARGET_WEBHOOK")

# Initialisation des composants
rt_data = RealTimeData(symbol='solusdt')
trading_ai = TradingAIAutoLearn()

@app.route("/", methods=["GET"])
def dashboard():
    return jsonify({
        "status": "ACTIF",
        "mode": "APPRENTISSAGE" if not trading_ai.model else "PRODUCTION",
        "signaux_traités": trading_ai.signal_count,
        "précision": f"{trading_ai.accuracy * 100:.1f}%" if trading_ai.accuracy else "N/A"
    })

@app.route("/webhook", methods=["POST"])
def handle_signal():
    try:
        # Configuration du signal
        signal_data = request.get_json()
        signal_type = signal_data.get('type', 'long').upper()
        
        # Vérification des données temps réel
        current_data = rt_data.get_recent_data()
        if not current_data:
            return jsonify({"erreur": "Données marché indisponibles"}), 503
            
        # Calcul des indicateurs
        indicators = calculate_indicators(rt_data.df)
        
        # Gestion de l'apprentissage
        if not trading_ai.model_ready:
            trading_ai.add_training_data({
                **indicators,
                "signal_type": signal_type,
                "timestamp": datetime.now().isoformat()
            })
            action = "APPRENTISSAGE"
            confidence = 0.0
        else:
            # Prédiction avec l'IA
            confidence = trading_ai.predict({
                'rsi': indicators['rsi'],
                'macd': indicators['macd_diff'],
                'variation': indicators['variation_1m']
            })
            action = "TRANSMIS" if confidence >= 0.75 else "REJETÉ"
        
        # Journalisation détaillée
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type_signal": signal_type,
            "prix": current_data['price'],
            "confiance": f"{confidence * 100:.1f}%" if confidence else "N/A",
            "action": action,
            "indicateurs": indicators
        }
        save_trading_log(log_entry)
        
        # Transmission du signal validé
        if action == "TRANSMIS" and WEBHOOK_TARGET:
            requests.post(WEBHOOK_TARGET, json={
                "action": signal_type,
                "confidence": confidence,
                "price": current_data['price'],
                "timestamp": log_entry['timestamp']
            })
        
        return jsonify(log_entry)

    except Exception as e:
        return jsonify({"erreur": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
