from app import db
from datetime import datetime, timezone

class Admin(db.Model):
    __tablename__ = 'admin'

    RUT = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    conductores_asignados = db.relationship('AdminConductor', foreign_keys='AdminConductor.admin_id', back_populates='admin_asigna')
    envios_gestionados = db.relationship('AdminEnvio', back_populates='admin')
