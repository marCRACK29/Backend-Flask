from flask import Flask
from flask_restful import Api, Resource

names = {"1":{"peso":2.5, "dimensiones":"30x20x10", "ruta_id":1}}

class EntregaResource(Resource):
    def get(self, name):
        return names[name]

    def post(self):
        return {"data": "Posted"}