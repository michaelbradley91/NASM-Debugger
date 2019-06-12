from typing import Callable

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from resource_manager import get_resource


class QuitAction(QAction):
    def __init__(self, quit_app: Callable, parent: QObject):
        super().__init__(QIcon(get_resource("quit.svg")), "&Quit", parent)
        self.setShortcut("Ctrl+Q")
        self.setStatusTip("Close NASM Debugger")
        self.triggered.connect(quit_app)
