from app import db
from datetime import datetime, timezone

class EntregaModel(db.Model):
    __tablename__ = 'entregas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    ruta_id = db.Column(db.Integer, nullable=False)
    # Estado actual del paquete (1: En preparación, 2: En tránsito, 3: Entregado)
    estado_id = db.Column(db.Integer, nullable=False, default=1)
    peso = db.Column(db.Numeric(10,2), nullable=False)
    dimensiones = db.Column(db.String(50), nullable=False)
    fecha_envio = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))