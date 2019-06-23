from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from service_locator import get_resource
from widgets.appearance.appearance_window import AppearanceWindow


class AppearanceAction(QAction):
    def __init__(self, parent: QObject):
        super().__init__(QIcon(get_resource("appearance.svg")), "&Appearance", parent)
        self.parent = parent
        self.setShortcut("Ctrl+A")
        self.setStatusTip("Change the appearance of NASM debugger.")
        self.triggered.connect(self.open_appearance_dialog)

    def open_appearance_dialog(self):
        """ Open the appearance dialog so the user can change colours, fonts and entire themes. """
        appearance_window = AppearanceWindow(self.parent)
        appearance_window.show()
