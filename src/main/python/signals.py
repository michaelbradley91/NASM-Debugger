from PyQt5.QtCore import pyqtSignal, QObject

from settings.constants import SettingScope


class Signals(QObject):
    """ Holds signals shared between objects. Allows for simpler communication between objects. """
    __exit_action_signal = pyqtSignal()
    __file_selected_signal = pyqtSignal(str)
    __folder_opened_signal = pyqtSignal(str)
    __setting_changed_signal = pyqtSignal(SettingScope, str)

    @property
    def exit_action_signal(self) -> pyqtSignal:
        return self.__exit_action_signal

    @property
    def file_selected_signal(self) -> pyqtSignal:
        return self.__file_selected_signal

    @property
    def folder_opened_signal(self) -> pyqtSignal:
        return self.__folder_opened_signal

    @property
    def setting_changed_signal(self):
        return self.__setting_changed_signal
