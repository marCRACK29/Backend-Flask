import requests

BASE = "http://127.0.0.1:5000/"

nuevo_envio = {
    "remitente_id" : "21.595.999-3",
    "ruta_id" : 5,
    "conductor_id": "15.123.123-5"
}

response = requests.post(BASE + "api/envios", json=nuevo_envio)

print("Status code:", response.status_code)

try:
    print(response.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response.text)
