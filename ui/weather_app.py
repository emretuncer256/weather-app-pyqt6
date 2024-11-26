from .settings_dialog_ui import Ui_Dialog
from .weatherapp_ui import Ui_MainWindow
from PyQt6.QtWidgets import QDialog, QMainWindow, QDialogButtonBox
from PyQt6.QtGui import QIcon
from assets.icons import Icons


class WeatherApp(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(str(Icons.APP_ICON)))


class SettingsDialog(Ui_Dialog, QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

    def setSaveEvent(self, func):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).clicked.connect(func)

    def setCancelEvent(self, func):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(func)