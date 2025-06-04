from flask_restful import Resource, reqparse
from app.services.cliente_service import actualizar_direccion, actualizar_correo, obtener_envios_cliente, obtener_info_cliente
from typing import Tuple, Dict, Any, Union

class ClienteDireccionResource(Resource):
    def put(self) -> Tuple[Dict[str, Any], int]:
        """
        Actualiza la dirección de un cliente.
        
        Returns:
            Tuple[Dict[str, Any], int]: Respuesta y código de estado HTTP
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "rut_cliente",
            type=str,
            required=True,
            help="El RUT del cliente es requerido"
        )
        parser.add_argument(
            "calle",
            type=str,
            required=True,
            help="La calle es requerida"
        )
        parser.add_argument(
            "numero_domicilio",
            type=int,
            required=True,
            help="El número de domicilio es requerido"
        )
        parser.add_argument(
            "ciudad",
            type=str,
            required=True,
            help="La ciudad es requerida"
        )
        parser.add_argument(
            "region",
            type=str,
            required=True,
            help="La región es requerida"
        )
        parser.add_argument(
            "codigo_postal",
            type=int,
            required=True,
            help="El código postal es requerido"
        )
        
        try:
            args = parser.parse_args()
            resultado = actualizar_direccion(args["rut_cliente"], args)
            return resultado, 200
            
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

class ClienteCorreoResource(Resource):
    def put(self) -> Tuple[Dict[str, Any], int]:
        """
        Actualiza el correo electrónico de un cliente.
        
        Returns:
            Tuple[Dict[str, Any], int]: Respuesta y código de estado HTTP
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "rut_cliente",
            type=str,
            required=True,
            help="El RUT del cliente es requerido"
        )
        parser.add_argument(
            "nuevo_correo",
            type=str,
            required=True,
            help="El nuevo correo electrónico es requerido"
        )
        
        try:
            args = parser.parse_args()
            resultado = actualizar_correo(args["rut_cliente"], args["nuevo_correo"])
            return resultado, 200
            
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

class ClienteEnviosResource(Resource):
    def get(self) -> Tuple[Union[Dict[str, Any], list], int]:
        """
        Obtiene todos los envíos de un cliente.
        
        Returns:
            Tuple[Union[Dict[str, Any], list], int]: Respuesta y código de estado HTTP
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "rut_cliente",
            type=str,
            required=True,
            location="args",
            help="El RUT del cliente es requerido"
        )
        
        try:
            args = parser.parse_args()
            envios = obtener_envios_cliente(args["rut_cliente"])
            
            if envios is None:
                return {"mensaje": "No tienes envíos registrados"}, 200
                
            return envios, 200
            
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

class ClienteInfoResource(Resource):
    def get(self) -> Tuple[Dict[str, Any], int]:
        """
        Obtiene la información básica de un cliente (RUT, nombre y correo).
        
        Returns:
            Tuple[Dict[str, Any], int]: Respuesta y código de estado HTTP
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "rut_cliente",
            type=str,
            required=True,
            location="args",
            help="El RUT del cliente es requerido"
        )
        
        try:
            args = parser.parse_args()
            info_cliente = obtener_info_cliente(args["rut_cliente"])
            return info_cliente, 200
            
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500
