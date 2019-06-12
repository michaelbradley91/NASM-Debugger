from typing import Callable

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QAction


class QuitAction(QAction):
    def __init__(self, quit_app: Callable, parent: QObject):
        super().__init__("&Quit", parent)
        self.setShortcut("Ctrl+Q")
        self.setStatusTip("Close NASM Debugger")
        self.triggered.connect(quit_app)
