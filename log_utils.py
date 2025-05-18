import json
from datetime import datetime
import os

def log_signal(symbol, interval, price, variation, analysis):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "interval": interval,
        "price": price,
        "variation": variation,
        "analysis": analysis
    }
    
    print(f"📝 Log: {json.dumps(log_entry, indent=2)}")

def save_signal_to_json(symbol, interval, price, variation, analysis):
    try:
        filename = "signals_history.json"
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "interval": interval,
            "price": price,
            "variation": variation,
            "analysis": analysis
        }
        
        if os.path.exists(filename):
            with open(filename, "r+") as file:
                existing = json.load(file)
                existing.append(data)
                file.seek(0)
                json.dump(existing, file, indent=2)
        else:
            with open(filename, "w") as file:
                json.dump([data], file, indent=2)
                
    except Exception as e:
        print(f"Erreur de sauvegarde : {str(e)}")

def get_last_price_variation(current_price):
    # Implémentation basique (à améliorer)
    return 0.0  # Temporaire
