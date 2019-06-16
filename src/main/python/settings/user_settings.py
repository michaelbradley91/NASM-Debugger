import os
from enum import Enum

from PyQt5.QtCore import QObject, QSettings
from PyQt5.QtWidgets import QWidget
from injector import inject

from configuration import Configuration
from helpers.settings_helpers import save_widget, restore_widget


class Key(Enum):
    """
    All the settings key used. It is important they are all unique
    Note that these do not correspond exactly to keys due to save shortcuts for widgets.
    """
    window = "window"
    window_vertical_splitter = "window.vertical_splitter"
    window_horizontal_splitter = "window.horizontal_splitter"
    last_folder_opened = "last_folder_opened"
    project = "project"
    project_tree = "project.tree"


class Default:
    """
    Stores all the defaults for base user settings.
    """
    last_folder_opened = os.path.expanduser("~")


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

    def save(self, key: Key, value: any):
        """ Save a value in the user's settings """
        self.__store.setValue(key.value, value)

    def get(self, key: Key, default: any = None):
        """ Get a value from the user's settings. Returns the given default if not found, or None otherwise """
        return self.__store.value(key.value, default)

    def save_widget(self, widget: QWidget, group: Key):
        """ Save a widget's state to the user's settings. """
        save_widget(self.__store, widget, group.value)

    def restore_widget(self, widget: QWidget, group: Key):
        """ Restore a widget's state from a user's settings. """
        restore_widget(self.__store, widget, group.value)

    def file_path(self) -> str:
        """ Get the file path for the user settings. """
        return self.__store.fileName()

    def sync(self):
        self.__store.sync()
