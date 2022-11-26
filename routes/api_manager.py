import uuid
from datetime import datetime
from flask import jsonify, abort, request, Blueprint
from validate_email import validate_email
from enums import enums

api_manager = Blueprint('api_manager', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return api_manager


@api_manager.route('/sensors', methods=['GET', 'POST'])
def sensor_info():
    if request.method == 'GET':
        return "To get all sensors info"
    if request.method == 'POST':
        return "To add a new sensor in the system"


@api_manager.route('/measurements', methods=['GET', 'POST'])
def sensor_measurment():
    if request.method == 'GET':
        return "To get all measurements"
    if request.method == 'POST':
        return "To add a new measurment in the system"


@api_manager.route('/measurements/<string:type>', methods=['GET'])
def sensor_measurment_by_type(type):
    if request.method == 'GET':
        if type == enums.Type.Temperature or type == enums.Type.Humidity or type == enums.Type.Acoustic:
            return "To get {} sensor measurements".format(type)
        else:
            abort(400)


# http://127.0.0.1:5000/measurements/234.1234/1234.234
@api_manager.route('/measurements/<float:latitude>/<float:longtitude>', methods=['GET'])
def sensor_measurment_by_location(latitude, longtitude):
    if request.method == 'GET':
        try:
            latitude = float(latitude)
            longtitude  = float(longtitude)
            return "To get sensor measurements at {}, {}".format(latitude, longtitude)
        except ValueError as e:
            abort(400)


# http://127.0.0.1:5000/measurements/1669377978.513893
@api_manager.route('/measurements/<float:time_stamp>', methods=['GET'])
def sensor_measurment_by_timestamp(time_stamp):
    if request.method == 'GET':
        try:
            date = datetime.fromtimestamp(time_stamp, tz=None)
            return "To get sensor measurements at {}".format(date)
        except ValueError:
            abort(400)