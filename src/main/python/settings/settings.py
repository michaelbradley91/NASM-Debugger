"""
The root of all NASM Debugger settings.
"""

from PyQt5.QtCore import QObject
from injector import inject

from settings.user_settings import UserSettings


class Settings(QObject):
    """ Root class of all configurable settings. """
    @inject
    def __init__(self, user_settings: UserSettings):
        super().__init__()
        self.__user_settings = user_settings

    @property
    def user(self) -> UserSettings:
        return self.__user_settings
