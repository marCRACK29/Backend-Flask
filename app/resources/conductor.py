from flask_restful import Resource, reqparse
from app.services.conductor_service import obtener_envios_en_curso, actualizar_estado_envio_conductor
from typing import Tuple, Dict, Any, Union

class ConductorEnvioResource(Resource):
    def get(self) -> Tuple[Union[Dict[str, Any], list], int]:
        """
        Obtiene los envíos en curso de un conductor.
        
        Returns:
            Tuple[Union[Dict[str, Any], list], int]: Respuesta y código de estado HTTP
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "conductor_id",
            type=str,
            required=True,
            location="args",
            help="El RUT del conductor es requerido"
        )
        
        try:
            args = parser.parse_args()
            conductor_id = args["conductor_id"]
            
            # Validar formato del RUT (formato básico)
            if not conductor_id.replace(".", "").replace("-", "").isdigit():
                return {"error": "El RUT del conductor tiene un formato inválido"}, 400
                
            envios = obtener_envios_en_curso(conductor_id)

            if envios is None:
                return {"mensaje": "No tienes envíos en curso"}, 200
                
            return envios, 200
            
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

    def get_en_curso(self) -> Tuple[Union[Dict[str, Any], list], int]:
        """
        Obtiene los envíos en curso de un conductor.
        
        Returns:
            Tuple[Union[Dict[str, Any], list], int]: Respuesta y código de estado HTTP
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "conductor_id",
            type=str,
            required=True,
            location="args",
            help="El RUT del conductor es requerido"
        )
        
        try:
            args = parser.parse_args()
            conductor_id = args["conductor_id"]
            
            # Validar formato del RUT (formato básico)
            if not conductor_id.replace(".", "").replace("-", "").isdigit():
                return {"error": "El RUT del conductor tiene un formato inválido"}, 400
                
            envios = obtener_envios_en_curso(conductor_id)

            if envios is None:
                return {"mensaje": "No tienes envíos en curso"}, 200
                
            return envios, 200
            
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

class ConductorActualizarEstadoResource(Resource):
    def put(self, envio_id: int) -> Tuple[Dict[str, Any], int]:
        """
        Permite a un conductor actualizar el estado de un envío asignado a él.
        
        Args:
            envio_id (int): ID del envío a actualizar
            
        Returns:
            Tuple[Dict[str, Any], int]: Respuesta y código de estado HTTP
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "conductor_id",
            type=str,
            required=True,
            help="El RUT del conductor es requerido"
        )
        parser.add_argument(
            "nuevo_estado",
            type=str,
            required=True,
            help="El nuevo estado del envío es requerido"
        )
        
        try:
            args = parser.parse_args()
            conductor_id = args["conductor_id"]
            nuevo_estado = args["nuevo_estado"]
            
            # Validar formato del RUT (formato básico)
            if not conductor_id.replace(".", "").replace("-", "").isdigit():
                return {"error": "El RUT del conductor tiene un formato inválido"}, 400
            
            resultado = actualizar_estado_envio_conductor(envio_id, conductor_id, nuevo_estado)
            return resultado, 200
            
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except LookupError as le:
            return {"error": str(le)}, 404
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500
