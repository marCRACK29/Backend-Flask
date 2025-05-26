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
python3 run.py
```

## Instrucciones para actualizar la base de datos: 
- Entrar al entorno virtual e instalar los requerimientos, ahi esta el paquete Flask-Migrate. 
- Luego, ejecutar el archivo reset_db.py.
```
python3 reset_db.py
```
- Una vez eso, les mostrara 3 instrucciones en la terminal, deben seguir los comandos. 
- Opcional: Una vez ejecutado los comandos, pueden revisar en dbeaver si se actualizó su base de datos. Debería aparecer las nuevas tablas Cliente, Admin, Conductor. Con respecto a la tabla usuario, ya no deberia aparecer porque se eliminó. 

## Instrucciones para correr con ngrok: 
Asumiendo que ya hicieron su cuenta e instalaron ngrok en sus dispositivos
- Entrar al entorno virtual
- Ejecutar run.py
- Ejecutar en otra terminal, dentro del directorio raiz: ngrok http 5000
- ngrok les dará un https. SOLO COMO EJEMPLO: https://63b6-191-116-73-47.ngrok-free.app -> http://localhost:5000  
- copiar solo el https y copiarlo en su .env, en la nueva variable: API_BASE_URL=https://63b6-191-116-73-47.ngrok-free.app/ 
- NOTEN QUE AL FINAL DEL HTTPS, USTED DEBE AGREGAR LA BARRA (/) MANUALMENTE. Es importante no olvidarse de la barra al final.
- Luego, deberían poder ejecutar el test_registro_usr.py exitosamente. 
