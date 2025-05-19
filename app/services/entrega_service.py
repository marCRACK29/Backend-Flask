from app import db
from app.models.entrega_model import EntregaModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import requests


def crear_entrega(usuario_id, ruta_id, peso, dimensiones):
    nueva_entrega = EntregaModel(
        usuario_id=usuario_id,
        ruta_id=ruta_id,
        peso=peso,
        dimensiones=dimensiones
    )
    try:
        db.session.add(nueva_entrega) # añadir objeto temporalmente a la bd
        db.session.commit() # hacer permanentes los cambios
        return nueva_entrega
    except IntegrityError:
        db.session.rollback()
        raise ValueError("No se pudo crear la entrega. Verifica que el usuario y la ruta existan")
    

def actualizar_estado_entrega(entrega_id, nuevo_estado):
    if nuevo_estado not in [1,2,3]:
        raise ValueError("Nuevo estado no es 1, 2 ni 3")
    
    try:
        entrega = EntregaModel.query.get(entrega_id)
        if not entrega:
            raise LookupError(f"Entrega con id {entrega_id} no encontrada")
        entrega.estado_id = nuevo_estado
        db.session.commit()
        return entrega.estado_id
    except SQLAlchemyError as e:
        db.session.rollback()
        raise RuntimeError("Error al actualizar el estado de la base de datos") from e

def obtener_entregas_por_usuario(usuario_id):
    if not isinstance(usuario_id, int) or usuario_id<=0:
        raise ValueError("El usuario_id debe ser entero positivo")
    try:
        entregas = EntregaModel.query.filter_by(usuario_id=usuario_id).all()
        
        if not entregas:
            return None
        
        return entregas
    except Exception as e:
        raise RuntimeError(f"Ocurrió un error al consultar las entregas: {str(e)}")
        
    