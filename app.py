from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
API_URL = "https://api.danny-avila.com/chat/completions"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Messaggio mancante"}), 400

    payload = {
        "model": "mistral",
        "messages": [{"role": "user", "content": message}]
    }

    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        ai_reply = resp.json()['choices'][0]['message']['content']
        return jsonify({"response": ai_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
