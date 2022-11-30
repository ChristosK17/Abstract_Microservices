import uuid
from datetime import datetime
from flask import jsonify, abort, request, Blueprint
from flask_restx import Api, Resource, fields, reqparse
from validate_email import validate_email
from enums import enums

api_manager = Blueprint('api_manager', __name__)

api = Api(api_manager, version="1.0", title="Abstract Microservices", description="Simple REST API",)

sensors = api.namespace("sensors", description="Abstract Microservices sensors")
measurements = api.namespace("measurements", description="Abstract Microservices measurements")

sensor_info_model = api.model('Sensor Info', {
    'sensorId': fields.Integer(required=True, description='Sensor Id'),
    'vendorName': fields.String(required=True, description='Vendors Name')
})

measurement_info_model = api.model('Measurement Info', {
    'sensorId': fields.Integer(required=True, description='Sensor Id'),
    'measurement': fields.Float(required=True, description='Measurement Name')
})

def get_blueprint():
    """Return the blueprint for the main app module"""
    return api_manager


@sensors.route('/')
class SensorInfo(Resource):

    '''Shows a list of all sensors, and lets you POST to add new sensors'''

    @sensors.marshal_list_with(sensor_info_model)
    def get(self):
        '''Get sensor information'''
        return "To get all sensors info"
    
    # curl -X POST localhost:5000/sensors -H "Content-Type: application/json" -d "{\"hello\": \"motherfucker\"}"
    @sensors.expect(sensor_info_model)
    @sensors.marshal_with(sensor_info_model, code=201)
    def post(self):
        '''To add a new sensor in the system'''
        return "To add a new sensor in the system " # + str(request.get_json(force=True))


@measurements.route('/')
class SensorMeasurement(Resource):
    
    '''Shows a list of all measurements, and lets you POST to add new measurements'''

    @sensors.marshal_list_with(measurement_info_model)
    def get(self):
        '''To get all measurement info'''
        return "To get all measurement info"
    
    @sensors.expect(measurement_info_model)
    @sensors.marshal_with(measurement_info_model, code=201)
    def post(self):
        '''To add a new measurement in the system'''
        return "To add a new measurement in the system " # + str(request.get_json(force=True))


@measurements.route('/<string:type>')
class SensorMeasurementByType(Resource):
    
    @sensors.marshal_list_with(measurement_info_model)
    def get(self, type):
        '''Get sensor measurements by sensor type'''
        print(type)
        if type == enums.Type.Temperature.name or type == enums.Type.Humidity.name or type == enums.Type.Acoustic.name:
            return "To get {} sensor measurements".format(type)
        else:
            api.abort(400)


# http://127.0.0.1:5000/measurements/234.1234/1234.234
@measurements.route('/<float:latitude>/<float:longtitude>')
class SensorMeasurementByLocation(Resource):

    @sensors.marshal_list_with(measurement_info_model)
    def get(self, latitude, longtitude):
        '''To get sensor measurements at lan, long'''
        try:
            latitude = float(latitude)
            longtitude  = float(longtitude)
            return "To get sensor measurements at {}, {}".format(latitude, longtitude)
        except ValueError as e:
            api.abort(400)


# http://127.0.0.1:5000/measurements/1669377978.513893
@measurements.route('/<float:time_stamp>')
class SensorMeasurementByTimestamp(Resource):

    @sensors.marshal_list_with(measurement_info_model)
    def get(self, time_stamp):
        '''To get sensor measurements at a date/time'''
        try:
            date = datetime.fromtimestamp(time_stamp, tz=None)
            return "To get sensor measurements at {}".format(date)
        except ValueError:
            api.abort(400)