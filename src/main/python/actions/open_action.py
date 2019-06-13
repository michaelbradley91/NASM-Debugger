from typing import Callable

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from service_locator import get_resource


class OpenAction(QAction):
    def __init__(self, open: Callable, parent: QObject):
        super().__init__(QIcon(get_resource("open_folder.png")), "&Open Folder", parent)
        self.setShortcut("Ctrl+O")
        self.setStatusTip("Open your project's folder.")
        self.triggered.connect(open)
