from app import db
from datetime import datetime, timezone

class Direccion(db.Model):
    __tablename__ = 'direcciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_rut = db.Column(db.String(12), db.ForeignKey('usuario.RUT'), nullable=False)
    calle = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    numero_departamento = db.Column(db.String(20))  # Para departamento, oficina, etc.
    comuna = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    codigo_postal = db.Column(db.String(10))
    indicaciones_adicionales = db.Column(db.String(200))  # Para indicaciones adicionales
    es_predeterminada = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relación con el usuario
    usuario = db.relationship('Usuario', backref=db.backref('direcciones', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_rut': self.usuario_rut,
            'calle': self.calle,
            'numero': self.numero,
            'numero_departamento': self.numero_departamento,
            'comuna': self.comuna,
            'ciudad': self.ciudad,
            'region': self.region,
            'codigo_postal': self.codigo_postal,
            'indicaciones_adicionales': self.indicaciones_adicionales,
            'es_predeterminada': self.es_predeterminada,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        } 