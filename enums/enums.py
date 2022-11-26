from enum import Enum
 
class Type(Enum):
    Temperature = 1
    Humidity = 2
    Acoustic = 3

class Unit(Enum):
    Celcius = 1
    Fahrenheit = 2
    Kelvin = 3
    AbsoluteM3 = 4 # Absolute humidity measured in (Mass of water vapor) gr / (Volume of moist air) m3
    AbsoluteKg = 5 # Absolute humidity measured in (Mass of water vapor) gr / (Mass of moist air) kg
    Relative = 6 # Relative humidity measured by percentage (%)
    Specific = 7 # (Specific humidity measured by water vapor mass) gr / (Total moist air parcel mass) kg
    AcousticUnit = 8