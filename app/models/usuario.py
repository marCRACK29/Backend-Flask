from app import db
from datetime import datetime, timezone

# Similar a declarar una tabla en pgsql
# Superclase
class Usuario(db.Model):
    __tablename__ = 'usuario'

    RUT = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)
    __mapper_args__ = { # para herencia en entidades
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo_usuario
    }
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


# Entidades hijas
class Cliente(Usuario):
    __tablename__ = 'cliente'

    RUT = db.Column(db.String(12), db.ForeignKey('usuario.RUT'), primary_key=True)
    numero_domicilio = db.Column(db.Integer, nullable=False)
    calle = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }

    # Relaciones con Envio
    envios_recibidos = db.relationship('Envio', foreign_keys="[Envio.receptor_id]",back_populates='receptor', lazy=True)
    envios_realizados = db.relationship('Envio', foreign_keys="[Envio.remitente_id]",back_populates='remitente', lazy=True)

class Conductor(Usuario):
    __tablename__ = 'conductor'

    RUT = db.Column(db.String(12), db.ForeignKey('usuario.RUT'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'conductor',
    }
    # Relacion con envío 
    envios_asignados = db.relationship('Envio', foreign_keys="[Envio.conductor_id]",back_populates='conductor')
    #Relación con admin: admin asigna un conductor
    asignaciones_admin = db.relationship('AdminConductor', back_populates='conductor_asignado')

class Admin(Usuario):
    __tablename__ = 'admin'

    RUT = db.Column(db.String(12), db.ForeignKey('usuario.RUT'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    #Relación con conductor: admin asigna un conductor
    conductores_asignados = db.relationship('AdminConductor', back_populates='admin_asigna')
    #Relacion con envío: admin gestiona un envío
    envios_gestionados = db.relationship('AdminEnvio', back_populates='admin')
