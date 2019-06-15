import os
from logging import Logger

from PyQt5.QtCore import QObject, pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication
from injector import inject

from configuration import Configuration


class UserSettings(QObject):
    """ The root of all user settings. """
    last_folder_opened_signal = pyqtSignal(str)

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        QSettings.setDefaultFormat(QSettings.IniFormat)
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope,
                          configuration.user_settings_directory)
        # We fake the application and organisation name to try and use a "nice" directory for settings.
        self.__user_settings_store = QSettings(QSettings.IniFormat, QSettings.UserScope,
                                               "settings", "", self)

    @property
    def last_folder_opened(self) -> str:
        return self.__user_settings_store.value("last_folder_opened", os.path.expanduser("~"))

    @last_folder_opened.setter
    def last_folder_opened(self, value: str):
        self.__user_settings_store.setValue("last_folder_opened", value)
        self.last_folder_opened_signal.emit(value)

    def file_path(self) -> str:
        """ Get the file path for the user settings. """
        return self.__user_settings_store.fileName()
