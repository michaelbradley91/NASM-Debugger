import json
import os
import pickle
from enum import Enum
from typing import Union

from PyQt5.QtCore import QObject, QSettings
from PyQt5.QtWidgets import QWidget
from injector import inject

from configuration import Configuration
from helpers.settings_helpers import save_widget, restore_widget, NOT_FOUND_VALUE


class Key(Enum):
    """
    All the settings key used. It is important they are all unique
    Note that these do not correspond exactly to keys due to save shortcuts for widgets and dynamic components.
    """
    window = "window"
    window_vertical_splitter = "window.vertical_splitter"
    window_horizontal_splitter = "window.horizontal_splitter"
    last_folder_opened = "last_folder_opened"
    project = "project"
    project_tree = "project.tree"
    editor = "editor"
    editor_open_files = "editor.open_files"
    editor_current_file = "editor.current_file"
    editor_tab = "editor.tab"
    tools = "tools"
    appearance = "appearance"


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

    def save(self, key: Union[Key, str], value: any):
        """ Save a value in the user's settings. """
        self.__store.setValue(UserSettings.__key_value(key), value)

    def save_as_json(self, key: Union[Key, str], value: any):
        """ Saves the given object in json. Useful for simple types when not natively supported. """
        self.__store.setValue(UserSettings.__key_value(key), json.dumps(value))

    def save_as_binary(self, key: Union[Key, str], value: any):
        """ Saves the given object in binary. Useful when other formats are not possible. """
        self.__store.setValue(UserSettings.__key_value(key), pickle.dumps(value))

    def get(self, key: Union[Key, str], default: any = None) -> any:
        """ Get a value from the user's settings. Returns the given default if not found, or None otherwise. """
        return self.__store.value(UserSettings.__key_value(key), default)

    def get_from_json(self, key: Union[Key, str], default: any = None):
        """ Get a value from stored JSON. """
        value = self.__store.value(UserSettings.__key_value(key), NOT_FOUND_VALUE)
        if value == NOT_FOUND_VALUE:
            return default
        else:
            return json.loads(value)

    def get_from_binary(self, key: Union[Key, str], default: any = None):
        """ Get a value from stored binary."""
        value = self.__store.value(UserSettings.__key_value(key), NOT_FOUND_VALUE)
        if value == NOT_FOUND_VALUE:
            return default
        else:
            return pickle.loads(value)

    def save_widget(self, widget: QWidget, group: Union[Key, str]):
        """ Save a widget's state to the user's settings. """
        save_widget(self.__store, widget, UserSettings.__key_value(group))

    def restore_widget(self, widget: QWidget, group: Union[Key, str]):
        """ Restore a widget's state from a user's settings. """
        restore_widget(self.__store, widget, UserSettings.__key_value(group))

    def file_path(self) -> str:
        """ Get the file path for the user settings. """
        return self.__store.fileName()

    @staticmethod
    def __key_value(key: Union[Key, str]):
        return key if isinstance(key, str) else key.value

    def clear(self):
        """
        Remove all keys from settings. This is a simple way to ensure the settings file does not grow due
        to dynamic keys.
        """
        for key in list(self.__store.allKeys()):
            self.__store.remove(key)

    def sync(self):
        """ Ensure the settings file is updated. """
        self.__store.sync()
