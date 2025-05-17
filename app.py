from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def ver_hora():
    return render_template('index.html')

@app.route('/ayuda')
def ayuda():
    return "API para consultar la zona horaria. Usa /zonas para ver opciones."

@app.route('/zonas', methods=['GET'])
def obtener_zonas():
    response = requests.get('https://worldtimeapi.org/api/timezone', verify=False)
    zonas = response.json()
    return jsonify(zonas)

@app.route('/hora', methods=['GET'])
def obtener_hora():
    zona = request.args.get('zona')
    if not zona:
        return jsonify({"error": "Debes indicar la zona horaria en 'zona'"}), 400
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
    app.run(debug=True)
