from app import db
from datetime import datetime, timezone

class EstadoEnvio(db.Model):
    __tablename__ = 'estado_envio'

    id = db.Column(db.Integer, primary_key=True)
    envio_id = db.Column(db.Integer, db.ForeignKey('envio.id'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_entrega.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
 