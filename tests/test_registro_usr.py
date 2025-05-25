import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

nuevo_cliente = {
    "RUT": "21.595.999-3",
    "nombre": "juanito",
    "correo": "juan@example.com",
    "contraseña": "holacliente",
    "tipo_usuario": "cliente",
    "numero_domicilio": 444,
    "calle": "Calle Verdadera",
    "ciudad": "Santiago",
    "region": "RM",
    "codigo_postal": 1234888
}

nuevo_conductor = {
    "RUT": "15.123.123-5",
    "nombre": "Conductor Ejemplo",
    "correo": "conductor@example.com",
    "contraseña": "holaconductor",
    "tipo_usuario": "conductor"
}

response_cliente = requests.post(BASE + "api/auth/register", json=nuevo_cliente)
response_conductor = requests.post(BASE + "api/auth/register", json=nuevo_conductor)

def print_response(label, response):
    print("Status code:", response.status_code)
    try:
        print(f"Respuesta para {label}:", response.json())
    except Exception:
        print(f"Respuesta para {label} (texto):", response.text)

print_response("cliente", response_cliente)
print_response("conductor", response_conductor)
