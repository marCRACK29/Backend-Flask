from app import db
from datetime import datetime, timezone

class EstadoEnvio(db.Model):
    __tablename__ = 'estado_envio'

    id = db.Column(db.Integer, primary_key=True)
    envio_id = db.Column(db.Integer, db.ForeignKey('envio.id_envio'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id_estado'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    envio = db.relationship('Envio', back_populates='historial_estados')
    estado = db.relationship('Estado', back_populates='envios') 