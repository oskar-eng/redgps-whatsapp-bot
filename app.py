from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Mensaje recibido:", data)

    if data and "body" in data and "from" in data:
        incoming_msg = data["body"].lower()
        sender = data["from"]

        # Mensaje de respuesta simple
        reply = "👋 ¡Hola! Soy tu asistente Lia, ¿en qué puedo ayudarte hoy?"

        return jsonify({
            "to": sender,
            "message": reply
        })

    return "ok", 200

@app.route("/")
def home():
    return "Bot de WhatsApp activo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

