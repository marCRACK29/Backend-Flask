# app/services/entrega_service.py

import psycopg2
from flask import jsonify

def crear_entrega(data):
    try:
        conn = psycopg2.connect(
            dbname="gestion_logistica",
            user="tu_usuario",
            password="tu_password",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        query = """
            INSERT INTO paquetes (usuario_id, peso, dimensiones, ruta_id, estado_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """
        estado_id_inicial = 1  # Asumimos "En preparación"
        cur.execute(query, (
            data["usuario_id"],
            data["peso"],
            data["dimensiones"],
            data["ruta_id"],
            estado_id_inicial
        ))

        paquete_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "mensaje": "Entrega creada exitosamente",
            "paquete_id": paquete_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
