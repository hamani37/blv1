import json
import os

LOG_FILE = 'live_data.json'

def log_signal(signal, price, indicators, decision, explanation):
    log_entry = {
        'signal': signal,
        'price': price,
        'indicators': indicators,
        'decision': decision,
        'explanation': explanation
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_last_price_variation(current_price):
    if not os.path.exists(LOG_FILE):
        return 0.0

    with open(LOG_FILE, 'r') as f:
        data = json.load(f)

    if not data:
        return 0.0

    last_price = data[-1]['price']
    variation = ((current_price - last_price) / last_price) * 100
    return round(variation, 2)
