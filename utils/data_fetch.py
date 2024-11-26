import requests
import json
from PyQt6.QtCore import QThread, pyqtSignal
from models.weather import CurrentWeather
from utils.constants import API_PATH, URL

with open(API_PATH) as f:
    API_KEY = f.read()


def fetchCurrentWeather(city, lang='tr'):
    query = {
        'q': city,
        'key': API_KEY,
        'lang': lang
    }
    r = requests.get(URL + '/current.json', params=query)
    data = json.loads(r.text)
    return CurrentWeather.fromJson(data)


def fetchIcon(url):
    return requests.get("https:" + url, stream=True).content


if __name__ == "__main__":
    print(fetchIcon("//cdn.weatherapi.com/weather/64x64/day/122.png"))
