import sys
import json
import threading

from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (
    QApplication,
)
from enums.temp_type import TempType
from ui.weather_app import WeatherApp, SettingsDialog
from utils.data_fetch import fetchCurrentWeather, fetchIcon


class MainWindow(WeatherApp):
    def __init__(self):
        super().__init__()

        with open('appsettings.json') as f:
            self.default_settings = json.load(f)

        self.location = self.default_settings['default_location']
        self.lang = self.default_settings['default_lang']
        self.temp_type = TempType.CELSIUS if self.default_settings[
                                                 'default_unit'] == "Celcius" else TempType.FAHRENHEIT

        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.setSaveEvent(self.save_settings)
        self.settings_dialog.setCancelEvent(self.settings_dialog.close)

        self.statusbar = self.statusBar()

        self.actionPreferences.triggered.connect(self.open_settings)

        self.current_weather = fetchCurrentWeather(self.location, self.lang)
        self.refresh_data()

        self.button_location.clicked.connect(self.search_by_location)

    def search_by_location(self):
        if self.lineEdit_location.text():
            self.location = self.lineEdit_location.text()
            threading.Thread(target=self.refresh_data).start()

    def refresh_data(self):
        self.current_weather = fetchCurrentWeather(self.location, self.lang)
        self.update_ui()

    def _getIconImage(self, ):
        image = QImage()
        image.loadFromData(fetchIcon(self.current_weather.condition.icon))
        return image

    def update_ui(self):
        if self.current_weather is not None:
            self.label_location.setText(self.current_weather.location.getCity())
            self.label_cond_icon.setPixmap(QPixmap(self._getIconImage()))
            self.label_cond_text.setText(self.current_weather.condition.text)
            self.label_temp.setText(str(self.current_weather.temp_c) if self.temp_type == TempType.CELSIUS else str(
                self.current_weather.temp_f))
            self.label_temp_type.setText(self.temp_type.value)
            self.label_feels_val.setText(
                str(self.current_weather.feelslike_c) if self.temp_type == TempType.CELSIUS else str(
                    self.current_weather.feelslike_f))
            self.label_feels_type.setText(self.temp_type.value)
            self.label_humidity_val.setText(str(self.current_weather.humidity))
            self.statusbar.showMessage("Done", 1500)

    def open_settings(self):
        self.settings_dialog.lineEdit_def_loc.setText(self.default_settings['default_location'])
        self.settings_dialog.cbx_unit.setCurrentText(self.default_settings['default_unit'])
        self.settings_dialog.show()

    def save_settings(self):
        self.default_settings['default_location'] = self.settings_dialog.lineEdit_def_loc.text()
        self.default_settings[
            'default_unit'] = "Celcius" if self.settings_dialog.cbx_unit.currentText() == "C°" else "Fahrenheit"
        print(self.default_settings['default_unit'])

        self.location = self.default_settings['default_location']
        self.temp_type = TempType.CELSIUS if self.default_settings['default_unit'] == "Celcius" else TempType.FAHRENHEIT
        print(TempType.CELSIUS if self.default_settings['default_unit'] == "Celcius" else TempType.FAHRENHEIT)

        self._save_settings_to_file()
        threading.Thread(target=self.refresh_data).start()
        self.settings_dialog.close()

    def _save_settings_to_file(self):
        self.default_settings = {
            "default_location": self.default_settings['default_location'],
            "default_unit": self.default_settings['default_unit'],
            "default_lang": self.lang
        }
        print(self.default_settings)
        with open('appsettings.json', 'w') as f:
            json.dump(self.default_settings, f, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
