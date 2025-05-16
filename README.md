# Paquimóvil

### Integrantes:

- Alan Ibacache
- Braian Urra
- Gabriel Castillo
- Sebastián Vega
- Marcos Martínez

### Instrucciones de uso:

- Asegurarse de tener python3 instalado.
- Activar el entorno virtual en la terminal con:
```
    source .venv/bin/activate
```
- Instalar los requerimientos con: 
```
    pip install -r requirements.txt
```
- Comprueben con: 
```
    python3 -m flask --version
```
- Ejecutar la app: 
```
chmod +x devserver.sh
./devserver.sh
```
- Mostrara la url: http://127.0.0.1:5000/, pero no buscarla por el navegador, ya que da error. Lo cual es correcto, ya que no estamos haciendo nada "gráfico". 
- Hay dos ejemplos solo para la autenticación (resources/auth.py, services/auth_service.py).