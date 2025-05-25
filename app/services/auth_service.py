from app import db
from app.models import Cliente, Conductor, Admin
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
import requests

def login_usuario(email, password):
    response = requests.post('http://servicio-auth:5000/login', json={
        'email': email,
        'password': password
    })
    return response.json(), response.status_code

def registrar_conductor(RUT, nombre, correo, contraseña):
    # Validar que no exista el usuario
    if Conductor.query.filter_by(correo=correo).first():
        raise ValueError("El correo ya esta registrado.")
    if Conductor.query.get(RUT):
        raise ValueError("El RUT ya esta registrado.")
    
    c_hash = generate_password_hash(contraseña)
    
    nuevo_conductor = Conductor(
        RUT=RUT,
        nombre=nombre,
        correo=correo,
        contraseña=c_hash
    )
    
    try: 
        db.session.add(nuevo_conductor)
        db.session.commit()
        return nuevo_conductor    
    
    except IntegrityError as e:
        db.session.rollback()
        print("ERROR DE INTEGRIDAD:", str(e))
        raise ValueError("No se pudo registrar el usuario. Verifica que RUT o correo no estén duplicados.")

def registrar_admin(RUT, nombre, correo, contraseña):
    # Validar que no exista el usuario
    if Admin.query.filter_by(correo=correo).first():
        raise ValueError("El correo ya esta registrado.")
    if Admin.query.get(RUT):
        raise ValueError("El RUT ya esta registrado.")
    
    c_hash = generate_password_hash(contraseña)
    
    nuevo_admin = Admin(
        RUT=RUT,
        nombre=nombre,
        correo=correo,
        contraseña=c_hash
    )
    
    try: 
        db.session.add(nuevo_admin)
        db.session.commit()
        return nuevo_admin    
    
    except IntegrityError as e:
        db.session.rollback()
        print("ERROR DE INTEGRIDAD:", str(e))
        raise ValueError("No se pudo registrar el usuario. Verifica que RUT o correo no estén duplicados.")

def registrar_cliente(RUT, nombre, correo, contraseña, numero_domicilio, calle, ciudad, region, codigo_postal):
    # Validar que no exista el usuario
    if Cliente.query.filter_by(correo=correo).first():
        raise ValueError("El correo ya esta registrado.")
    if Cliente.query.get(RUT):
        raise ValueError("El RUT ya esta registrado.")
    
    c_hash = generate_password_hash(contraseña)

    nuevo_cliente = Cliente(
        RUT=RUT,
        nombre=nombre,
        correo=correo,
        contraseña=c_hash,
        numero_domicilio=numero_domicilio,
        calle=calle,
        ciudad=ciudad,
        region=region,
        codigo_postal=codigo_postal
    )

    try: 
        db.session.add(nuevo_cliente)
        db.session.commit()
        return nuevo_cliente
        
    except IntegrityError as e:
        db.session.rollback()
        print("ERROR DE INTEGRIDAD:", str(e))
        raise ValueError("No se pudo registrar el usuario. Verifica que RUT o correo no estén duplicados.")