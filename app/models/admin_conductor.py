from app import db

class AdminConductor():
    __tablename__ = 'admin_conductor'

    id = db.Column(db.Integer, primary_key=True)
    id_conductor = db.Column(db.String(12), db.ForeignKey('conductor.RUT'), nullable=False)
    id_admin = db.Column(db.String(12), db.ForeignKey('conductor.RUT'), nullable=False)

    conductor_asignado = db.relationship('Conductor', back_populates='asignaciones_admin')
    admin_asigna =  db.relationship('Admin', back_populates='conductores_asignados')