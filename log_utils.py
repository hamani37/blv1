import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def save_trading_log(log_data):
    log_entry = {
        "horodatage": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": log_data['type_signal'],
        "prix": log_data['prix'],
        "confiance": log_data['confiance'],
        "action": log_data['action'],
        "indicateurs": log_data['indicateurs'],
        "variation_réelle": "N/A"
    }

    with open('trading_logs.jsonl', 'a') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    logger.debug(f"Log entry saved: {log_entry}")
