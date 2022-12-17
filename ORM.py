class SensorORM:
    def convert(data) -> str:
        query = list(data.values())
        query[-1] = f"ARRAY[{tuple(eval(query[-1]).values())}]::loc[]"
        return query

print(SensorORM.convert({'sensorId': '0X6E7', 'type': 'Temperature', 'vendorName': 'Texas Instruments', 'vendorEmail': 'texas@instruments.com', 'description': 'This sensor is inside a house', 'location': "{'latitude': 32.4574, 'longtitude': 20.6583}"}))