"""
app.py
--------
Aplicación Flask que permite consultar la hora actual de distintas zonas horarias
utilizando la API pública de WorldTimeAPI. Si el servicio no responde, la aplicación
muestra la hora local del dispositivo del usuario, actualizándola en tiempo real
desde el frontend.

Desarrollado por: Daniela Castillo
Fecha: Mayo 2025
"""
from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def ver_hora():
    """
    Ruta principal que entrega la página HTML de interfaz.
    """
    return render_template('index.html')

@app.route('/ayuda')
def ayuda():
    """
    Ruta auxiliar que entrega información básica del uso de la API.
    """
    return "API para consultar la zona horaria. Usa /zonas para ver opciones."

@app.route('/zonas', methods=['GET'])
def obtener_zonas():
    """
    Llama a la API pública de WorldTimeAPI para obtener una lista de zonas horarias disponibles.

    Returns:
        JSON: Lista de zonas horarias (strings).
    """
    try:
        response = requests.get('https://worldtimeapi.org/api/timezone', verify=False)
        response.raise_for_status()
        zonas = response.json()
        return jsonify(zonas)
    except requests.RequestException as e:
        return jsonify({"error": f"No se pudo obtener la lista de zonas. Detalle: {str(e)}"}), 500
@app.route('/hora', methods=['GET'])
def obtener_hora():
    """
    Devuelve la hora actual para una zona horaria específica.

    Parámetros (por query string):
        zona (str): nombre de la zona horaria, por ejemplo "America/Santiago".

    Returns:
        JSON: con 'zona' y 'hora_actual' si esta bien
              o mensaje de error si falla.
    """
    zona = request.args.get('zona')
    if not zona:
        return jsonify({"error": "Debes indicar la zona horaria en 'zona'"}), 400
    # Construimos la URL con la zona seleccionada
    url = f'https://worldtimeapi.org/api/timezone/{zona}'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Zona horaria no válida"}), 404
    datos = response.json()
    return jsonify({
        "zona": zona,
        "hora_actual": datos["datetime"]
    })

if __name__ == '__main__':
   #solo para desarrollo local
    app.run(debug=True)
