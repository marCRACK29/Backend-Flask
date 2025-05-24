from app import db
from app.models.usuario import Usuario, Cliente, Conductor, Admin
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
import requests
from sqlalchemy import inspect

# ESTE ES SOLO UN EJEMPLO
def login_usuario(email, password):
    response = requests.post('http://servicio-auth:5000/login', json={
        'email': email,
        'password': password
    })
    return response.json(), response.status_code


def registrar_usuario(RUT, nombre, correo, contraseña, tipo_usuario, numero_domicilio=None, calle=None, ciudad=None, region=None, codigo_postal=None):

    print("Base de datos conectada a:", db.engine.url)
    print("Tablas disponibles:", inspect(db.engine).get_table_names())
    print("Usuarios en la base actualmente:")
    print([u.correo for u in Usuario.query.all()])

    if Usuario.query.filter_by(correo=correo).first():
        raise ValueError("El correo ya esta registrado.")
    if Usuario.query.get(RUT):
        raise ValueError("El RUT ya esta registrado.")
    
    c_hash = generate_password_hash(contraseña)
    
    if tipo_usuario == "cliente":
        nuevo_usuario = Cliente(
            RUT=RUT,
            nombre=nombre,
            correo=correo,
            contraseña=c_hash,
            tipo_usuario=tipo_usuario,
            numero_domicilio=numero_domicilio,
            calle=calle,
            ciudad=ciudad,
            region=region,
            codigo_postal=codigo_postal
        )
    elif tipo_usuario == "conductor":
        nuevo_usuario = Conductor(
            RUT=RUT,
            nombre=nombre,
            correo=correo,
            contraseña=c_hash,
            tipo_usuario=tipo_usuario
        )
    elif tipo_usuario == "admin":
        nuevo_usuario = Admin(
            RUT=RUT,
            nombre=nombre,
            correo=correo,
            contraseña=c_hash,
            tipo_usuario=tipo_usuario
        )
    else:
        nuevo_usuario = Usuario(
            RUT=RUT,
            nombre=nombre,
            correo=correo,
            contraseña=c_hash,
            tipo_usuario=tipo_usuario
        )

    try: 
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario
    except IntegrityError as e:
        db.session.rollback()
        print("ERROR DE INTEGRIDAD:", str(e))
        raise ValueError("No se pudo registrar el usuario. Verifica que RUT o correo no estén duplicados.")