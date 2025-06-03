from app import db

class Estado(db.Model):
    __tablename__ = 'estado_entrega'

    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(20), nullable=False)

    envios = db.relationship('Envio', back_populates='estado')

    def to_dict(self):
        return {
            'id': self.id,
            'estado': self.estado
        }