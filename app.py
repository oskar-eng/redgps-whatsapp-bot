from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Variables de entorno de UltraMsg
INSTANCE_ID = os.getenv("ULTRA_INSTANCE_ID")
TOKEN = os.getenv("ULTRA_TOKEN")
ACTIVOS_API_URL = os.getenv("ACTIVOS_API_URL")  # URL de la API en Render

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data or "body" not in data:
        return jsonify({"status": "no data"})

    message = data["body"].get("message")
    sender = data["body"].get("from")

    if not message or not sender:
        return jsonify({"status": "invalid message"})

    if message.lower().startswith("bateria"):
        partes = message.split()
        if len(partes) >= 2:
            placa = partes[1].strip()
            return consultar_bateria(placa, sender)
        else:
            return send_whatsapp(sender, "⚠️ Debes indicar una placa. Ej: bateria CE-025067")

    return send_whatsapp(sender, "ℹ️ Hola! Puedes consultar así: bateria CE-025067")


def consultar_bateria(placa, telefono):
    try:
        response = requests.get(ACTIVOS_API_URL)
        activos = response.json()

        for activo in activos:
            if activo.get("unidad") == placa:
                mensaje = f"🔋 Unidad {placa}\nBatería: {activo['bateria']}%\n⏰ Último reporte: {activo['ultimo_reporte']}"
                return send_whatsapp(telefono, mensaje)

        return send_whatsapp(telefono, f"❌ No se encontró la unidad {placa}")

    except Exception as e:
        return send_whatsapp(telefono, f"❌ Error al consultar la batería: {str(e)}")


def send_whatsapp(to, message):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    payload = {
        "token": TOKEN,
        "to": to,
        "body": message
    }
    try:
        r = requests.post(url, data=payload)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
