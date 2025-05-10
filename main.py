from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("✅ Signal reçu :", data)
    return jsonify({"status": "reçu", "détail": data}), 200

if __name__ == '__main__':
    app.run()
