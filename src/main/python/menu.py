from PyQt5.QtWidgets import QMainWindow

from actions.appearance_action import AppearanceAction
from actions.open_action import OpenAction
from actions.quit_action import QuitAction


class Menu:
    """ This is a wrapper class for configuring the menu on the main window. """
    def __init__(self, window: QMainWindow):
        self.window = window
        self.menu = self.window.menuBar()

        self.file_menu = self.add_file_menu()
        self.settings_menu = self.add_settings_menu()

    def add_file_menu(self):
        file_menu = self.menu.addMenu("&File")
        file_menu.addAction(OpenAction(self.window))
        file_menu.addAction(QuitAction(self.window))
        return file_menu

    def add_settings_menu(self):
        settings_menu = self.menu.addMenu("&Settings")
        settings_menu.addAction(AppearanceAction(self.window))
        return settings_menu
