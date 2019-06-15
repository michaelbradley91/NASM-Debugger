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
    def __init__(self, app: QApplication, configuration: Configuration, logger: Logger):
        super().__init__()
        QSettings.setDefaultFormat(QSettings.IniFormat)
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope,
                          configuration.user_settings_directory)
        self.__user_settings_store = QSettings(QSettings.IniFormat, QSettings.UserScope,
                                               "settings", "", self)
        logger.info(f"Settings stored in {self.__user_settings_store.fileName()}")

    @property
    def last_folder_opened(self) -> str:
        return self.__user_settings_store.value("last_folder_opened", os.path.expanduser("~"))

    @last_folder_opened.setter
    def last_folder_opened(self, value: str):
        self.__user_settings_store.setValue("last_folder_opened", value)
        self.last_folder_opened_signal.emit(value)