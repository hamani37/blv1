import json
from collections import Counter

def log_signal(signal_data):
    try:
        with open("signals_log.json", "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(signal_data)
    with open("signals_log.json", "w") as f:
        json.dump(logs, f, indent=2)

def print_stats():
    try:
        with open("signals_log.json", "r") as f:
            logs = json.load(f)

        count = Counter([s["signal"] for s in logs])
        total = len(logs)
        print(f"📊 Stats (total {total} signaux) : {dict(count)}")

    except:
        print("Aucune stat disponible")
