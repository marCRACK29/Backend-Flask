from app import db
from datetime import datetime, timezone

# Similar a declarar una tabla en pgsql
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    RUT = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))