# PaquiMóvil

### Integrantes: 
 - Braian Urra
 - Alan Ibacache
 - Sebastián Vega
 - Gabriel Castillo 
 - Marcos Martínez
 
### Descripción general
Este repositorio se compone de la parte lógica de un proyecto de dos partes, dividiéndose principalmente en archivos de modelos, servicios y recursos, permitiendo así una estructura con una división de responsabilidades clara y limpia, que implícitamente lo vuelve escalable y modular. Para trabajar este apartado, decidimos usar el framework Flask, esto debido a su fácil uso, flexibilidad y sus librerías (Flask-RESTful).

### Instrucciones de ejecución
-Copiar repositorio frontend y backend (links respectivos) de forma local.
-Instalar ngrok.
-Instalar requerimientos del proyecto (estos se encuentran en el backend), el comando para esto es "pip install -r requirements.txt".
-Ejecutar ngrok, comando "ngrok http 5000".
-Actualizar archivo .env de backend con el https de ngrok en API_BASE_URL (con "/" al final de esta dirección).
-Crear y activar un entorno virtual para el backend.
python3 -m venv .venv
source .venv/bin/activate
-Ejecutar backend (en otra terminal), comando "python3 run.py".

