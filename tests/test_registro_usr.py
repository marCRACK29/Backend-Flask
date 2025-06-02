import requests
import os
from dotenv import load_dotenv
import random
import time

load_dotenv()
BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/")

# Generar un timestamp único para evitar duplicaciones
timestamp = int(time.time())

# Cliente con todos los datos requeridos
nuevo_cliente = {
    "RUT": f"21.595.999-4",
    "nombre": f"Cliente Test {timestamp}",
    "correo": f"cliente{timestamp}@example.com",
    "contraseña": "holacliente",
    "numero_domicilio": 444,
    "calle": "Calle Verdadera",
    "ciudad": "Santiago",
    "region": "RM",
    "codigo_postal": 1234888
}

# Conductor sin datos de dirección (no los necesita)
nuevo_conductor = {
    "RUT": f"15.123.123-7",
    "nombre": f"Conductor Test {timestamp}",
    "correo": f"conductor{timestamp}@example.com",
    "contraseña": "holaconductor"
}

# Admin sin datos de dirección (no los necesita)
nuevo_admin = {
    "RUT": f"12.345.{random.randint(100, 999)}-{random.randint(0, 9)}",
    "nombre": f"Admin Test {timestamp}",
    "correo": f"admin{timestamp}@example.com",
    "contraseña": "holaadmin"
}

def print_response(label, response):
    print(f"\n=== {label.upper()} ===")
    print("Status code:", response.status_code)
    try:
        print("Respuesta JSON:", response.json())
    except Exception:
        print("Respuesta texto:", response.text)
    print("=" * 30)

def limpiar_base_datos():
    """Opcional: función para limpiar usuarios de prueba"""
    # Aquí podrías implementar una llamada a un endpoint de limpieza
    # o usar directamente la base de datos si tienes acceso
    pass

# Realizar las pruebas
print("Iniciando pruebas de registro...")
print(f"Timestamp único: {timestamp}")

# Limpiar datos previos (opcional)
# limpiar_base_datos()

response_cliente = requests.post(BASE + "api/auth/register/cliente", json=nuevo_cliente)
print_response("cliente", response_cliente)

response_conductor = requests.post(BASE + "api/auth/register/conductor", json=nuevo_conductor)
print_response("conductor", response_conductor)

response_admin = requests.post(BASE + "api/auth/register/admin", json=nuevo_admin)
print_response("admin", response_admin)

# Prueba con cliente sin dirección (debe fallar)
cliente_sin_direccion = {
    "RUT": f"20.111.{random.randint(100, 999)}-{random.randint(0, 9)}",
    "nombre": f"Cliente Sin Direccion {timestamp}",
    "correo": f"sin_direccion{timestamp}@example.com",
    "contraseña": "password123"
}

response_error = requests.post(BASE + "api/auth/register/cliente", json=cliente_sin_direccion)
print_response("cliente sin dirección (error esperado)", response_error)

# Prueba de duplicación (debe fallar)
print("\n=== PRUEBA DE DUPLICACIÓN ===")
response_duplicado = requests.post(BASE + "api/auth/register/cliente", json=nuevo_cliente)
print_response("cliente duplicado (error esperado)", response_duplicado)