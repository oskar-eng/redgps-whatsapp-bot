from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot conectado y esperando mensajes 💬"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("\n📩 Webhook recibido:", data)

        message = data.get("body", {}).get("text")
        sender = data.get("body", {}).get("from")

        if message and sender:
            print(f"📨 Mensaje recibido: {message} de {sender}")

            if message.lower().startswith("bateria"):
                respuesta = f"🔋 Hola! La batería de la unidad es 85% (ejemplo). [Hora: {datetime.datetime.now().strftime('%H:%M:%S')}]"
            else:
                respuesta = "🤖 Hola, soy tu asistente de RedGPS. Puedes escribirme 'bateria [placa]' para comenzar."

            enviar_mensaje(sender, respuesta)

        return jsonify({"status": "ok"})
    except Exception as e:
        print("❌ Error en webhook:", str(e))
        return jsonify({"status": "error", "error": str(e)}), 500

def enviar_mensaje(telefono, mensaje):
    print(f"\n📤 Enviando respuesta a {telefono}: {mensaje}")

    url = "https://api.ultramsg.com/instance111839/messages/chat"
    payload = {
        "token": "r4wm825i3lqivpku",
        "to": telefono,
        "body": mensaje
    }

    try:
        r = requests.post(url, data=payload)
        print("✅ Enviado:", r.text)
    except Exception as e:
        print("❌ Error al enviar mensaje:", str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

