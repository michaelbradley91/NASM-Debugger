import os

from PyQt5.QtCore import QObject, pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication
from injector import inject

from configuration import Configuration


class UserSettings(QObject):
    """ The root of all user settings. """
    last_folder_opened_signal = pyqtSignal(str)

    @inject
    def __init__(self, app: QApplication, configuration: Configuration):
        super().__init__()
        self.__user_settings_store = QSettings(QSettings.IniFormat, QSettings.UserScope,
                                               app.organizationName(), app.applicationName(), self)
        self.__user_settings_store.setPath(QSettings.IniFormat, QSettings.UserScope,
                                           os.path.join(configuration.user_settings_directory, "settings.ini"))

    @property
    def last_folder_opened(self) -> str:
        return self.__user_settings_store.value("last_folder_opened", os.path.expanduser("~"))

    @last_folder_opened.setter
    def last_folder_opened(self, value: str):
        self.__user_settings_store.setValue("last_folder_opened", value)
        self.last_folder_opened_signal.emit(value)