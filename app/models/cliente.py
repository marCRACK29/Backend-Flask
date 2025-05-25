from app import db
from datetime import datetime, timezone

class Cliente(db.Model):
    __tablename__ = 'cliente'

    RUT = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    numero_domicilio = db.Column(db.Integer, nullable=False)
    calle = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.Integer, nullable=False)

    envios_recibidos = db.relationship('Envio', foreign_keys='Envio.receptor_id', back_populates='receptor', lazy=True)
    envios_realizados = db.relationship('Envio', foreign_keys='Envio.remitente_id', back_populates='remitente', lazy=True)