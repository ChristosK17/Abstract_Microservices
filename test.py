from flask import Flask, redirect, url_for, request, send_from_directory, make_response, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from routes import api_manager

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/Abstract_Microservices_Swagger.json'
CONFIG = {'app_name': "Abstract Microservices"}
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, CONFIG)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.register_blueprint(api_manager.get_blueprint())

# Error Code Handlers

@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

# @app.route("/")
# def hello_world():
#     return "Dis de api :)"

# @app.route("/static/")
# def send_static(path):
#     return send_from_directory("static", path)


# @app.route("/sensor", methods = ['GET', 'POST'])
# def sensor_information():
#     if request.method == 'GET':
#         return "To get sensors info"
#     if request.method == 'POST':
#         return "To send sensors info"


# @app.route("/measurment", methods = ['GET', 'POST'])
# def sensor_reading():
#     if request.method == 'GET':
#         return "To get sensors measurments"
#     if request.method == 'POST':
#         return "To send sensors measurments"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)