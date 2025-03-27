from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# UltraMsg
ULTRA_TOKEN = "r4wm825i3lqivpku"
ULTRA_INSTANCE = "instance111839"
ULTRA_API = f"https://api.ultramsg.com/{ULTRA_INSTANCE}/messages/chat"

# RedGPS
REDGPS_API = "https://redgps-proxy.onrender.com/activos"

# Enviar mensaje por WhatsApp
def enviar_whatsapp(to, mensaje):
    payload = {
        "token": ULTRA_TOKEN,
        "to": to,
        "body": mensaje
    }
    requests.post(ULTRA_API, data=payload)

# Buscar por placa en RedGPS
def buscar_por_placa(placa):
    try:
        response = requests.get(REDGPS_API)
        if response.status_code == 200:
            data = response.json()
            for unidad in data:
                if unidad.get("unidad", "").lower() == placa.lower():
                    return unidad
        return None
    except Exception as e:
        return None

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data and "body" in data and "from" in data:
        mensaje = data["body"].strip().lower()
        numero = data["from"]

        if mensaje.startswith("bateria"):
            partes = mensaje.split()
            if len(partes) >= 2:
                placa = " ".join(partes[1:]).upper()
                unidad = buscar_por_placa(placa)
                if unidad:
                    respuesta = f"🔋 Batería: {unidad['bateria']}%\n"
                    respuesta += f"📅 Último reporte: {unidad['ultimo_reporte']}\n"
                    respuesta += f"🚛 Unidad: {unidad['unidad']}"
                else:
                    respuesta = "No se encontró la unidad especificada."
            else:
                respuesta = "Por favor, indica la placa. Ej: bateria CE-123456"

            enviar_whatsapp(numero, respuesta)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

