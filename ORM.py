import datetime
from enums.enums import Unit

class SensorORM:
    def convert(data) -> str:
        query = list(data.values())
        query[-1] = tuple(eval(query[-1]).values()) #f"ARRAY[{tuple(eval(query[-1]).values())}]::loc[]"
        return query

    def reconstruct(data):
        out = []
        for item in data:
            out.append({"sensorId": item[0], "type": item[1], "vendorName": item[2], "vendorEmail": item[3], "description": item[4], "location": {"latitude", eval(item[5])[0], "longitude", eval(item[5])[1]}})
        return out

class MeasurementORM:
    def convert(data) -> str:
        query = list(data.values())
        query[2] = tuple(eval(query[2]).values()) #f"ARRAY[{tuple(eval(query[-1]).values())}]::loc[]"
        query[3] = str(datetime.datetime.fromtimestamp(query[3]))
        return query

    def reconstruct(data):
        out = []
        for item in data:
            index = item[3].replace("(", "").replace(")", "").split(",")
            out.append({"id": item[0], "sensorId": item[1], "measurementType": item[2], "measurementValue": {"value": index[0], "unit": index[1]}, "measurementDate": int(round(item[4].timestamp())), "description": item[5]})
        return out

if __name__ == "__main__":
    print(SensorORM.convert({'sensorId': '0X6E7', 'type': 'Temperature', 'vendorName': 'Texas Instruments', 'vendorEmail': 'texas@instruments.com', 'description': 'This sensor is inside a house', 'location': "{'latitude': 32.4574, 'longtitude': 20.6583}"}))
    print(SensorORM.reconstruct([('0X6E7', 'Temperature', 'Texas Instruments', 'texas@instruments.com', 'This sensor is inside a house', '(32.4574,20.6583)'), ('0X6E7', 'Temperature', 'Texas Instruments', 'texas@instruments.com', 'This sensor is inside a house', '(32.4574,20.6583)')]))
    print(MeasurementORM.convert({"sensorId": "0X6E7", "measurementType": "Temperature", "measurementValue": "{'measurement': 27.8, 'unit': 'Celcius'}", "measurementDate": 1671125670, "description": "This sensor is inside a house"}))
    print(MeasurementORM.reconstruct([(1, '0X6E7', 'Temperature', '(27.8,Celcius)', datetime.datetime(2004, 10, 19, 10, 23, 54), 'This sensor is inside a house'), (2, '0X6E7', 'Temperature', '(27.8,Celcius)', datetime.datetime(2004, 10, 19, 10, 23, 54), 'This sensor is inside a house')]))
