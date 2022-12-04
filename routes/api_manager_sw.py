import sys
import uuid
from datetime import datetime
from flask import jsonify, abort, request, Blueprint
from flask_restx import Api, Resource, fields, reqparse
from validate_email import validate_email
from enums import enums
#from api_key_protection import api_key_protection as protect

api_manager = Blueprint('api_manager', __name__)

api = Api(api_manager, version="1.0", title="Abstract Microservices", description="Simple REST API",)

sensors = api.namespace("sensors", description="Abstract Microservices sensors")
measurements = api.namespace("measurements", description="Abstract Microservices measurements")

sensor_info_model = api.model('Sensor Info', {
    'sensorId': fields.String(required=True, description='Sensor Id', example="0X6E7"),
    'type': fields.String(required=True, description='Sensor type Enum->(Temperature, Humidity or Acoustic)', example="Temperature"),
    'vendorName': fields.String(required=True, description='Vendors Name', example="Texas Instruments"),
    'vendorEmail': fields.String(required=True, description='Vendors Email', example="texas@instruments.com"),
    'description': fields.String(required=True, description='Description of sensor', example="This sensor is inside a house"),
    'location': fields.String(required=True, description="{'latitude': <float>, 'longtitude': <float>}", example="{'latitude': 32.4574, 'longtitude': 20.6583}")
})


measurement_info_model = api.model('Measurement Info', {
    #'Id': fields.String(required=True, description='Measurement Id (Configured by the database)'),
    'sensorId': fields.String(required=True, description='Sensor Id', example="0X6E7"),
    'readingType': fields.String(required=True, description='Sensor type Enum->(Temperature, Humidity or Acoustic)', example="Temperature"),
    'readingValue': fields.String(required=True, description="{'measurement': <float>, 'unit': <Celcius, Kelvin, Fahrenheit, AbsoluteM3, AbsoluteKg, Relative, Specific, UNIT1, UNIT2>}", example="{'measurement': <float>, 'unit': 'Celcius'}"),
    'readingDate': fields.Float(required=True, description="Timestamp (5134512.12512541)", example="5134512.12512541"),
    'description': fields.String(required=True, description='Description of sensor', example="This sensor is inside a house")
})

def get_blueprint():
    """Return the blueprint for the main app module"""
    return api_manager

#@protect.require_appkey
@sensors.route('/')
class SensorInfo(Resource):

    '''Shows a list of all sensors, and lets you POST to add new sensors'''

    @sensors.marshal_list_with(sensor_info_model)
    def get(self):
        '''Get sensor information'''
        return "To get all sensors info"

    @sensors.expect(sensor_info_model)
    @sensors.marshal_with(sensor_info_model, code=201)
    def post(self):
        '''To add a new sensor in the system'''
        try:
            if not (api.payload["type"] == enums.Type.Temperature.name or api.payload["type"] == enums.Type.Humidity.name or api.payload["type"] == enums.Type.Acoustic.name):
                api.abort(400)
            if not validate_email(api.payload["vendorsEmail"]):
                api.abort(400)
        except Exception as e:
            api.abort(400, custom=e)
        return "To add a new sensor in the system "


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
        return "To add a new measurement in the system "


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

# curl -X POST localhost:5000/sensors -H "Content-Type: application/json" -d "{\"hello\": \"motherfucker\"}"