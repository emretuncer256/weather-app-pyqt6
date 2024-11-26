import os
from pathlib import Path

ASSETS_PATH = Path(os.path.dirname(os.path.abspath(__file__))).parent / "assets"
ICONS_PATH = ASSETS_PATH / "icons"
API_PATH = Path(os.path.dirname(os.path.abspath(__file__))).parent / "API.txt"

URL = "https://api.weatherapi.com/v1"
