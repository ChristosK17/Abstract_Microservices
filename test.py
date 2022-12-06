from flask import Flask, redirect, url_for, request, send_from_directory, make_response, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from routes import api_manager_sw
from flask_restx  import Api
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title="Abstract Microservices", description="REST API for an IoT platform")

# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger_json_complete.json'
# CONFIG = {'app_name': "Abstract Microservices"}
# SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, CONFIG)

#app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.register_blueprint(api_manager_sw.get_blueprint())

# @app.route("/static/")
# def send_static(path):
#     return send_from_directory("static", path)


# Error Code Handlers

@api.errorhandler
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Bad request'}), 400)


@api.errorhandler
@api.doc(responses={404: 'Not found'})
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.errorhandler
@api.doc(responses={500: 'Server error'})
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)