import enum
from app import db

class EstadoEnum(enum.Enum):
    PREPARACION = "En preparación"
    TRANSITO = "En transito"
    ENTREGADO = "Entregado"

class Estado(db.Model):
    __tablename__ = 'estado_entrega'

    id_estado = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.Enum(EstadoEnum), nullable=False)

    envios = db.relationship('EstadoEnvio', back_populates='estado')