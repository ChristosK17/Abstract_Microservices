from flask import Flask, request
from flask_restx  import Api, Resource, fields
from datetime import datetime
from validate_email import validate_email
from enums.enums import Type, Unit
from ORM import SensorORM, MeasurementORM
import DBHandler
import unified_exceptions as ue
from flask_cors import CORS 
import sys


######################## Set up logging system ##########################

filename="Logs/logs.txt"
header = sys.argv[0].split("/")[-1]
exception_handler = ue.UnifiedExceptions(filename)


############################ Set up database ############################

sensors_table_name = "sensors"
measurements_table_name = "measurements"
sensors_schema = "(sensorId, type, vendorName, vendorEmail, description, location)"
measurements_schema = "(sensorId, measurementType, measurementValue, measurementDate, description)"

db = DBHandler.handler("abstractmicro", "table_schemas/sensor_datatype.txt", "table_schemas/measurement_datatype.txt", "table_schemas/sensor_table.txt", "table_schemas/measurement_table.txt")


############################### Set up api ###############################

app = Flask(__name__, template_folder='templates')

CORS(app) # CORS is used in order to allow all API calls


############################# Swagger setup ##############################

api = Api(app, version="1.0", title="Abstract Microservices", description="Simple REST API",)

sensors = api.namespace("sensors", description="Abstract Microservices sensors")
measurements = api.namespace("measurements", description="Abstract Microservices measurements")

sensor_info_model = api.model('Sensor Info', {
    'sensorId': fields.String(required=True, description='Sensor Id', example="0X6E7"),
    'type': fields.String(required=True, description='Sensor type Enum->(Temperature, Humidity or Acoustic)', example="Temperature"),
    'vendorName': fields.String(required=True, description='Vendors Name', example="Texas Instruments"),
    'vendorEmail': fields.String(required=True, description='Vendors Email', example="texas@instruments.com"),
    'description': fields.String(required=True, description='Description of sensor', example="This sensor is inside a house"),
    'location': fields.String(required=True, description="{'latitude': <float>, 'longitude': <float>}", example="{'latitude': 32.4574, 'longitude': 20.6583}")
})

measurement_info_model = api.model('Measurement Info', {
    #'Id': fields.String(required=True, description='Measurement Id (Configured by the database)'),
    'sensorId': fields.String(required=True, description='Sensor Id', example="0X6E7"),
    'measurementType': fields.String(required=True, description='Sensor type Enum->(Temperature, Humidity or Acoustic)', example="Temperature"),
    'measurementValue': fields.String(required=True, description="{'measurement': <float>, 'unit': <Celcius, Kelvin, Fahrenheit, AbsoluteM3, AbsoluteKg, Relative, Specific, UNIT1, UNIT2>}", example="{'measurement': 27.8, 'unit': 'Celcius'}"),
    'measurementDate': fields.Integer(required=True, description="Timestamp (ISO 8601). Better to pass a python timezone object. Ex:\n\nfrom datetime import datetime, timezone\ndt = datetime.now(timezone.utc)\ndatetime.datetime(2022, 12, 15, 16, 27, 45, 555500, tzinfo=datetime.timezone.utc)", example=1671125670),
    'description': fields.String(required=True, description='Description of sensor', example="This sensor is inside a house")
})


########################## API handling classes ##########################

@sensors.route('/')
class SensorInfo(Resource):

    '''Shows a list of all sensors, and lets you POST to add new sensors'''

    @exception_handler.handle
    @sensors.marshal_list_with(sensor_info_model)
    def get(self):

        '''Get sensor information'''
        
        exception_handler.debug(f"{header}\tGet all sensor info")
        data = db.get(sensors_table_name, set_limit= False if request.args.get('limit')==None else True , limit=request.args.get('limit'))
        
        return SensorORM.reconstruct(data)

    @sensors.expect(sensor_info_model)
    @sensors.marshal_with(sensor_info_model, code=201)
    def post(self):

        '''To add a new sensor in the system'''

        exception_handler.debug(f"{header}\tCreate a new sensor info")
        try:
            if not (api.payload["type"] == Type.Temperature.name or api.payload["type"] == Type.Humidity.name or api.payload["type"] == Type.Acoustic.name):
                exception_handler.warning("Bad request: Invalid type")
                api.abort(400)
            
            if not validate_email(api.payload["vendorEmail"]):
                exception_handler.warning(f"{header}\tBad request: Invalid email")
                api.abort(400)
            
            exception_handler.debug("f{header}\tInserting sensor")
            db.insert(sensors_table_name, sensors_schema, SensorORM.convert(api.payload))
       
        except Exception as e:
            exception_handler.warning(f"{header}\tBad request: {e}")
            api.abort(400, custom=e)
        
        return f"Sensor added successfully!\n{api.payload}"


@measurements.route('/')
class SensorMeasurement(Resource):
    
    '''Shows a list of all measurements, and lets you POST to add new measurements'''

    @exception_handler.handle
    @measurements.marshal_list_with(measurement_info_model)
    def get(self):

        '''To get all measurement info'''

        exception_handler.debug(f"{header}\tGet all measurements")
        data = db.get(sensors_table_name, set_limit= False if request.args.get('limit')==None else True , limit=request.args.get('limit'))
        
        return MeasurementORM.reconstruct(data)
    
    @measurements.expect(measurement_info_model)
    @measurements.marshal_with(measurement_info_model, code=201)
    def post(self):

        '''To add a new measurement in the system'''

        try:
            exception_handler.debug(f"{header}\tInserting measurement data from post request")
            db.insert(measurements_table_name, measurements_schema, MeasurementORM.convert(api.payload))

        except Exception as e:
            exception_handler.warning(f"{header}\tBad request: {e}")
            api.abort(400, custom=e)

        return f"Sensor added successfully!\n{api.payload}"


@measurements.route('/<string:type>')
class SensorMeasurementByType(Resource):
    
    @measurements.marshal_list_with(measurement_info_model)
    def get(self, type):

        '''Get sensor measurements by sensor type'''

        if not (type == Type.Temperature.name or type == Type.Humidity.name or type == Type.Acoustic.name):
            exception_handler.warning(f"{header}\tBad request")
            api.abort(400)

        exception_handler.debug(f"{header}\tGet all measurements by {type}")
        data = db.get(measurements_table_name, get_by="measurementType", value=type, set_limit = False if request.args.get('limit')==None else True , limit=request.args.get('limit'))
        
        return MeasurementORM.reconstruct(data)


@measurements.route('/<float:latitude>/<float:longitude>')
class SensorMeasurementByLocation(Resource):

    @measurements.marshal_list_with(measurement_info_model)
    def get(self, latitude, longitude):

        '''To get sensor measurements at lan, long'''

        try:
            latitude = float(latitude)
            longitude  = float(longitude)
            exception_handler.debug(f"{header}\tGet all measurements by lat: {latitude}, lon: {longitude}")
            return "To get sensor measurements at {}, {}".format(latitude, longitude)

        except ValueError as e:
            exception_handler.warning(f"{header}\tBad request: {e}")
            api.abort(400)


@measurements.route('/<int:time_stamp>')
class SensorMeasurementByTimestamp(Resource):

    @measurements.marshal_list_with(measurement_info_model)
    def get(self, time_stamp):

        '''To get sensor measurements at a date/time'''

        try:
            exception_handler.debug(f"{header}\tGet all measurements by {time_stamp}")
            data = db.get(measurements_table_name, get_by="measurementDate", value=str(datetime.fromtimestamp(time_stamp)), set_limit= False if request.args.get('limit')==None else True , limit=request.args.get('limit'))
            return MeasurementORM.reconstruct(data)

        except ValueError as e:
            exception_handler.warning(f"{header}\tBad request: {e}")
            api.abort(400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)