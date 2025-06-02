from app import db
from datetime import datetime, timezone

# Para almacenar coordenadas 
class Localizacion(db.Model):
    __tablename__ = 'localizacion'

    id = db.Column(db.Integer, primary_key=True)
    conductor_id = db.Column(db.String(12), db.ForeignKey('conductor.RUT'), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))