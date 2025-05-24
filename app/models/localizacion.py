from app import db
from datetime import datetime, timezone

# Para almacenar coordenadas 
class Localizacion(db.Model):
    __tablename__ = 'localizacion'

    id = db.Column(db.Integer, primary_key=True)
    envio_id = db.Column(db.Integer, db.ForeignKey('envio.id'), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))