from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Mensaje recibido:", data)  # Solo para verificar en los logs

    # Prueba básica: responder con un texto fijo a cualquier mensaje
    from_number = data.get('from')
    if from_number:
        send_message(from_number, "Hola, recibí tu mensaje ✅")
    return jsonify({'status': 'ok'}), 200

def send_message(to, message):
    import requests
    url = "https://api.ultramsg.com/instance111839/messages/chat"
    payload = {
        "token": "r4wm825i3lqivpku",  # <-- tu token aquí
        "to": to,
        "body": message
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers)
    print("Respuesta del envío:", response.text)

