from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Webhook recibido:", data)

    try:
        message = data.get("body", "").lower()
        sender = data.get("from", "")

        if "hola" in message:
            # Aquí iría el código para responder usando UltraMsg si deseas
            print(f"✅ Mensaje de saludo detectado de {sender}")
        else:
            print(f"🔹 Otro mensaje recibido: {message}")

    except Exception as e:
        print("❌ Error en webhook:", str(e))

    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=10000)
