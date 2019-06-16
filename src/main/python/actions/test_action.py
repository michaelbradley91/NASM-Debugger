from collections import Callable

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QAction


class TestAction(QAction):
    def __init__(self, test: Callable, parent: QObject):
        super().__init__("&Test", parent)
        self.setShortcut("Ctrl+T")
        self.setStatusTip("Run Test")
        self.triggered.connect(test)