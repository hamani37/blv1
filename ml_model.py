from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data or 'type' not in data:
        return jsonify({"status": "error", "message": "Type manquant"}), 400
    signal_type = data["type"]
    print(f"Signal reçu : {signal_type}")
    return jsonify({"status": "success", "received": signal_type})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
