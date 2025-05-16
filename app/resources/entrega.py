from flask_restful import Resource, reqparse


class EntregaResource(Resource):
    def post(self):
        parser = reqparse.RequestParser() # asegura que recibo la info que necesito
        # espero recibir los siguientes campos
        parser.add_argument("usuario_id", type=int, required=True, help="usuario_id es requerido") #help indica lo que le envio de vuelta
        parser.add_argument("peso", type=float, required=True, help="peso es requerido")           #si no recibo lo que necesitaba
        parser.add_argument("dimensiones", type=str, required=True, help="dimensiones son requeridas")
        parser.add_argument("ruta_id", type=int, required=True, help="ruta_id es requerida")

        args = parser.parse_args() # lee los datos de la solicitud, crea un diccionario con los datos

        return crear_entrega(args)