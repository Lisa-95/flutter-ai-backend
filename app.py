from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
API_URL = "https://api.danny-avila.com/chat/completions"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        print("📥 Request JSON:", data)

        message = data.get("message", "")
        if not message:
            return jsonify({"error": "Messaggio mancante"}), 400

        payload = {
            "model": "mistral",
            "messages": [{"role": "user", "content": message}]
        }

        print("🚀 Inviando payload all'API esterna...")
        resp = requests.post(API_URL, json=payload, timeout=30)
        print("🌐 Stato risposta API esterna:", resp.status_code)
        print("📄 Contenuto risposta API:", resp.text)

        resp.raise_for_status()
        response_json = resp.json()

        if 'choices' in response_json:
            ai_reply = response_json['choices'][0]['message']['content']
            return jsonify({"response": ai_reply})
        else:
            return jsonify({
                "error": "Risposta inattesa dal modello AI",
                "dettagli": response_json
            }), 502

    except Exception as e:
        print("❌ Errore:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
