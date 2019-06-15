import os

from PyQt5.QtCore import QObject, QSettings
from PyQt5.QtWidgets import QWidget
from injector import inject

from configuration import Configuration
from helpers.settings_helpers import save_widget, restore_widget


class UserSettings(QObject):
    """ The root of all user settings. """
    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        QSettings.setDefaultFormat(QSettings.IniFormat)
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope,
                          configuration.user_settings_directory)
        # We fake the application and organisation name to try and use a "nicer" directory for settings.
        # However, an organisation name is required to ensure this works properly on all systems.
        # See issues like this: https://www.qtcentre.org/threads/35300-QSplitter-restoreState()-not-working
        self.__store = QSettings(QSettings.IniFormat, QSettings.UserScope, "nasm", "settings", self)

    @property
    def last_folder_opened(self) -> str:
        return self.__store.value("last_folder_opened", os.path.expanduser("~"))

    @last_folder_opened.setter
    def last_folder_opened(self, value: str):
        self.__store.setValue("last_folder_opened", value)

    def save_widget(self, widget: QWidget, group: str):
        """ Save a widget's state to the user's settings. """
        save_widget(self.__store, widget, group)

    def restore_widget(self, widget: QWidget, group: str):
        """ Restore a widget's state from a user's settings. """
        restore_widget(self.__store, widget, group)

    def file_path(self) -> str:
        """ Get the file path for the user settings. """
        return self.__store.fileName()

    def sync(self):
        self.__store.sync()
