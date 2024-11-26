from dataclasses import dataclass
from datetime import datetime

TIME_FORMAT = r'%Y-%m-%d %H:%M'


@dataclass
class Location:
    name: str
    region: str | None
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime: datetime

    @staticmethod
    def fromJson(json):
        return Location(
            name=json['name'],
            region=json['region'],
            country=json['country'],
            lat=json['lat'],
            lon=json['lon'],
            tz_id=json['tz_id'],
            localtime=datetime.strptime(json['localtime'], TIME_FORMAT)
        )

    def toJson(self):
        return {
            'name': self.name,
            'region': self.region,
            'country': self.country,
            'lat': self.lat,
            'lon': self.lon,
            'tz_id': self.tz_id,
            'localtime': self.localtime.strftime(TIME_FORMAT)
        }

    def getCity(self):
        return self.country + "/" + self.name


@dataclass
class Condition:
    text: str
    icon: str
    code: int

    @staticmethod
    def fromJson(json):
        return Condition(
            text=json['text'],
            icon=json['icon'],
            code=json['code']
        )

    def toJson(self):
        return {
            'text': self.text,
            'icon': self.icon,
            'code': self.code
        }


@dataclass
class CurrentWeather:
    location: Location
    last_updated: datetime
    temp_c: float
    temp_f: float
    condition: Condition
    feelslike_c: float
    feelslike_f: float
    humidity: int

    @staticmethod
    def fromJson(json):
        return CurrentWeather(
            location=Location.fromJson(json['location']),
            last_updated=datetime.strptime(
                json['current']['last_updated'], TIME_FORMAT),
            temp_c=json['current']['temp_c'],
            temp_f=json['current']['temp_f'],
            condition=Condition.fromJson(json['current']['condition']),
            feelslike_c=json['current']['feelslike_c'],
            feelslike_f=json['current']['feelslike_f'],
            humidity=json['current']['humidity']
        )

    def toJson(self):
        return {'current': {
            'last_updated': self.last_updated.strftime(TIME_FORMAT),
            'temp_c': self.temp_c,
            'temp_f': self.temp_f,
            'condition': self.condition.toJson(),
            'feelslike_c': self.feelslike_c,
            'feelslike_f': self.feelslike_f,
            'humidity': self.humidity},
            'location': self.location.toJson()
        }
