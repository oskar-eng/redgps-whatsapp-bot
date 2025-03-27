from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configura tus credenciales de UltraMsg
ULTRAMSG_INSTANCE_ID = "instance111839"
ULTRAMSG_TOKEN = "r4wm825i3lqivpku"

# URL de tu API de activos
ACTIVOS_API_URL = "https://redgps-proxy.onrender.com/activos"

# Funciones de utilidad para enviar mensajes por UltraMsg
def enviar_mensaje(numero, mensaje):
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "body": mensaje
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200

# Funciones para interpretar comandos

def buscar_datos_por_placa(placa):
    try:
        response = requests.get(ACTIVOS_API_URL)
        data = response.json()
        for unidad in data:
            if placa.lower() in unidad["unidad"].lower():
                return unidad
    except:
        return None
    return None

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    mensaje = data.get("body", "").lower()
    numero = data.get("from", "")

    if mensaje.startswith("bateria"):
        partes = mensaje.split(" ")
        if len(partes) == 2:
            placa = partes[1]
            unidad = buscar_datos_por_placa(placa)
            if unidad:
                texto = f"🔋 Unidad {unidad['unidad']}\nBatería: {unidad['bateria']}%\n⏰ Último reporte: {unidad['ultimo_reporte']}"
            else:
                texto = f"No se encontró la unidad '{placa}'."
        else:
            texto = "Formato incorrecto. Escribe: bateria [placa]"

        enviar_mensaje(numero, texto)

    return jsonify({"status": "ok"})

# Esto es para pruebas locales. En Render, no es necesario ejecutar app.run
if __name__ == "__main__":
    app.run(debug=True)
