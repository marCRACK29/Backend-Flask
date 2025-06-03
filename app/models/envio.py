from app import db

class Envio(db.Model):
    __tablename__ = 'envio'

    id = db.Column(db.Integer, primary_key=True)
    # Almacena el id del usuario (su RUT)
    receptor_id = db.Column(db.String(12), db.ForeignKey('cliente.RUT'), nullable=False)
    remitente_id = db.Column(db.String(12), db.ForeignKey('cliente.RUT'), nullable=False)
    # Relación con conductor: un envío tiene un solo conductor. 
    conductor_id = db.Column(db.String(12), db.ForeignKey('conductor.RUT'))
    direccion_origen = db.Column(db.String(255), nullable=False)
    direccion_destino = db.Column(db.String(255), nullable=False)
    # Relación con estado actual
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_entrega.id'), nullable=False)

    # Receptor no siempre puede ser cliente, pero por ahora lo dejaremos así. CORREGIR
    receptor = db.relationship('Cliente', foreign_keys=[receptor_id], back_populates='envios_recibidos')
    remitente = db.relationship('Cliente', foreign_keys=[remitente_id], back_populates='envios_realizados')
    # Relación uno a muchos: un envío tiene muchos paquetes
    paquetes = db.relationship('Paquete', back_populates='envio', lazy=True)
    # Relación con estado actual
    estado = db.relationship('Estado', back_populates='envios')
    conductor = db.relationship('Conductor', foreign_keys=[conductor_id], back_populates='envios_asignados')
    gestiones_admin = db.relationship('AdminEnvio', back_populates='envio')
    