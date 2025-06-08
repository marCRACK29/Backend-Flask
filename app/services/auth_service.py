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

    # Obtener los datos de respuesta como JSON
    data = response.json()

    # Verificar el tipo de usuario según el campo 'kind'
    if data['kind'] == 'client':
        return registrar_cliente(...)
    elif data['kind'] == 'delivery':
        return registrar_conductor(...)
    elif data['kind'] == 'admin':
        return registrar_admin(...)

    # En caso de que el tipo no coincida con ninguno
    return data, response.status_code


def registrar_conductor(RUT, name, email, password):
    # Validar que no exista el usuario
    if Conductor.query.filter_by(email=email).first():
        raise ValueError("El email ya esta registrado.")
    if Conductor.query.get(RUT):
        raise ValueError("El RUT ya esta registrado.")
    
    c_hash = generate_password_hash(password)
    
    nuevo_conductor = Conductor(
        RUT=RUT,
        name=name,
        email=email,
        password=c_hash
    )
    
    try: 
        db.session.add(nuevo_conductor)
        db.session.commit()
        return nuevo_conductor    
    
    except IntegrityError as e:
        db.session.rollback()
        print("ERROR DE INTEGRIDAD:", str(e))
        raise ValueError("No se pudo registrar el usuario. Verifica que RUT o email no estén duplicados.")

def registrar_admin(RUT, name, email, password):
    # Validar que no exista el usuario
    if Admin.query.filter_by(email=email).first():
        raise ValueError("El email ya esta registrado.")
    if Admin.query.get(RUT):
        raise ValueError("El RUT ya esta registrado.")
    
    c_hash = generate_password_hash(password)
    
    nuevo_admin = Admin(
        RUT=RUT,
        name=name,
        email=email,
        password=c_hash
    )
    
    try: 
        db.session.add(nuevo_admin)
        db.session.commit()
        return nuevo_admin    
    
    except IntegrityError as e:
        db.session.rollback()
        print("ERROR DE INTEGRIDAD:", str(e))
        raise ValueError("No se pudo registrar el usuario. Verifica que RUT o email no estén duplicados.")

def registrar_cliente(RUT, name, email, password, numero_domicilio, calle, ciudad, region, codigo_postal):
    # Validar que no exista el usuario
    if Cliente.query.filter_by(email=email).first():
        raise ValueError("El email ya esta registrado.")
    if Cliente.query.get(RUT):
        raise ValueError("El RUT ya esta registrado.")
    
    c_hash = generate_password_hash(password)

    nuevo_cliente = Cliente(
        RUT=RUT,
        name=name,
        email=email,
        password=c_hash,
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
        raise ValueError("No se pudo registrar el usuario. Verifica que RUT o email no estén duplicados.")