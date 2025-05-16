from app import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
import requests

# ESTE ES SOLO UN EJEMPLO
def login_usuario(email, password):
    response = requests.post('http://servicio-auth:5000/login', json={
        'email': email,
        'password': password
    })
    return response.json(), response.status_code


def registrar_usuario(RUT, nombre, correo, contraseña):
    if Usuario.query.filter_by(correo=correo).first():
        raise ValueError("El correo ya esta registrado.")
    if Usuario.query.get(RUT):
        raise ValueError("El RUT ya esta registrado.")
    
    c_hash = generate_password_hash(contraseña)
    
    nuevo_usuario = Usuario(
        RUT = RUT,
        nombre=nombre, 
        correo=correo, 
        contraseña=c_hash
    )

    try: 
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario
    except IntegrityError:
        db.session.rollback()
        raise ValueError("No se pudo registrar el usuario. Verifica que RUT o correo no estén duplicados.")