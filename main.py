from flask import Flask, request
from ml_model import TradingIA

app = Flask(__name__)
model = TradingIA()

@app.route("/")
def index():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    signal_type = data.get("type")

    if signal_type not in ["long", "short"]:
        return "Signal invalide", 400

    print(f"✅ Signal reçu : {data}")
    result = model.process_signal(signal_type)
    print(result)
    return result, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
