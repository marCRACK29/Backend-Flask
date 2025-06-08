from app import db
from app.models import Cliente, Conductor, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask import current_app
import datetime
import jwt
import requests

def login_usuario(email, password):
    """
    Función de login local que busca en todas las tablas de usuarios
    """
    try:
        # Buscar usuario en todas las tablas
        usuario = None
        tipo_usuario = None
        
        # Buscar en Cliente
        cliente = Cliente.query.filter_by(correo=email).first()
        if cliente and check_password_hash(cliente.contraseña, password):
            usuario = cliente
            tipo_usuario = 'cliente'
        
        # Buscar en Conductor
        if not usuario:
            conductor = Conductor.query.filter_by(correo=email).first()
            if conductor and check_password_hash(conductor.contraseña, password):
                usuario = conductor
                tipo_usuario = 'conductor'
        
        # Buscar en Admin
        if not usuario:
            admin = Admin.query.filter_by(correo=email).first()
            if admin and check_password_hash(admin.contraseña, password):
                usuario = admin
                tipo_usuario = 'admin'
        
        if not usuario:
            return {'error': 'Credenciales inválidas'}, 401
        
        # Generar token JWT
        token = jwt.encode({
            'user_id': usuario.RUT,
            'email': usuario.correo,
            'tipo': tipo_usuario,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return {
            'message': 'Login exitoso',
            'token': token,
            'user': {
                'id': usuario.RUT,
                'name': usuario.nombre,
                'email': usuario.correo,
                'tipo': tipo_usuario
            }
        }, 200
        
    except Exception as e:
        return {'error': f'Error interno del servidor: {str(e)}'}, 500


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