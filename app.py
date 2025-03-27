from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Extraemos el número y el mensaje
    try:
        sender = data['from']
        message = data['body'].strip().lower()

        # Aquí simplemente respondemos algo fijo
        respuesta = "Hola, soy Lia 🤖. Estoy conectada y lista para ayudarte."

        # Enviar la respuesta por UltraMsg
        requests.post(
            "https://api.ultramsg.com/instance111839/messages/chat",
            data={
                "token": "r4wm825i3lqivpku",
                "to": sender,
                "body": respuesta
            }
        )
    except Exception as e:
        print("Error procesando mensaje:", e)

    return "ok"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
