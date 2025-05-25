from app import db
from datetime import datetime, timezone

class Conductor(db.Model):
    __tablename__ = 'conductor'

    RUT = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    envios_asignados = db.relationship('Envio', foreign_keys='Envio.conductor_id', back_populates='conductor', lazy=True)
    asignaciones_admin = db.relationship('AdminConductor', foreign_keys='AdminConductor.conductor_id', back_populates='conductor_asignado')