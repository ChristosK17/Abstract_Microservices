from flask import Flask, redirect, url_for, request, send_from_directory, make_response, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from routes import api_manager_sw
from flask_restx  import Api
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.register_blueprint(api_manager_sw.get_blueprint())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)