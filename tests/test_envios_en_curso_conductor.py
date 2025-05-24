import requests

BASE = "http://127.0.0.1:5000/"

conductor_id = "15.123.123-5"

response = requests.get(BASE + "api/conductor/envios/en-curso", params={"conductor_id": conductor_id})

print("Status code:", response.status_code)
try:
    print("Respuesta:", response.json())
except Exception as e:
    print("Error al leer JSON de respuesta:", str(e))
    print("Texto recibido:", response.text) 