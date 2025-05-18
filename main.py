from flask import Flask, request, jsonify
from log_utils import log_signal
from ml_model import ia_analyse_signal
from analyze_indicators import get_indicators
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'IA Trading Bot actif.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get('signal')
    pair = data.get('pair')
    price = float(data.get('price'))

    indicators = get_indicators(pair)

    decision, explanation = ia_analyse_signal(signal, price, indicators)

    log_signal(signal, price, indicators, decision, explanation)

    return jsonify({'status': 'ok', 'decision': decision, 'explanation': explanation})

if __name__ == '__main__':
    app.run(debug=True)
