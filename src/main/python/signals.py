from PyQt5.QtCore import pyqtSignal, QObject


class Signals(QObject):
    """ Holds signals shared between objects. Allows for simpler communication between objects. """
    __file_selected_signal = pyqtSignal(str)
    __folder_opened_signal = pyqtSignal(str)

    @property
    def file_selected_signal(self) -> pyqtSignal:
        return self.__file_selected_signal

    @property
    def folder_opened_signal(self) -> pyqtSignal:
        return self.__folder_opened_signal
