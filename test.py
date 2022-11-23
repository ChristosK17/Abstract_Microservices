from flask import Flask, redirect, url_for, request

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)


@app.route("/")
def hello_world():
    return "Dis de api :)"


@app.route("/sensor", methods = ['GET', 'POST'])
def sensor_information():
    if request.method == 'GET':
        return "To get sensors info"
    if request.method == 'POST':
        return "To send sensors info"


@app.route("/measurment", methods = ['GET', 'POST'])
def sensor_reading():
    if request.method == 'GET':
        return "To get sensors measurments"
    if request.method == 'POST':
        return "To send sensors measurments"

if __name__ == "__main__":
    app.run()