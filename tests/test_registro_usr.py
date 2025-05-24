import requests

BASE = "http://127.0.0.1:5000/"

nuevo_cliente = {
    "RUT": "15.123.123-4",
    "nombre": "Cliente Ejemplo",
    "correo": "cliente@example.com",
    "contraseña": "holacliente",
    "tipo_usuario": "cliente",
    "numero_domicilio": 123,
    "calle": "Calle Falsa",
    "ciudad": "Santiago",
    "region": "RM",
    "codigo_postal": 12345
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
