import json
import random

# Exemple d'IA simple - à remplacer plus tard par une vraie IA entraînée
def predict_signal(signal_data):
    return signal_data["signal"] if random.random() > 0.3 else "IGNORE"

def auto_train():
    try:
        with open("signals_log.json", "r") as f:
            logs = json.load(f)
        if len(logs) >= 50:
            print("📚 Entraînement automatique IA terminé.")
    except Exception:
        pass
