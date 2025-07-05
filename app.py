from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Modello gratuito AI ospitato su Hugging Face (senza chiavi)
API_URL = "https://huggingface.co/chat/"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        print("📥 Request JSON:", data)

        message = data.get("message", "")
        if not message:
            return jsonify({"error": "Messaggio mancante"}), 400

        # Formato compatibile con endpoint /chat di Hugging Face
        payload = {
            "inputs": f"[INST] {message} [/INST]",
            "parameters": {
                "do_sample": True,
                "max_new_tokens": 150,
                "temperature": 0.7
            }
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        print("🌐 Stato risposta:", response.status_code)
        print("📄 Contenuto:", response.text)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                ai_reply = data[0].get("generated_text", "Nessuna risposta generata.")
            else:
                ai_reply = "Risposta vuota dal modello."
            return jsonify({"response": ai_reply})
        else:
            return jsonify({"error": f"Errore dal modello AI: {response.status_code}"}), 502

    except Exception as e:
        print("❌ Errore:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
