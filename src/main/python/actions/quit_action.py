from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from service_locator import get_resource, signals


class QuitAction(QAction):
    def __init__(self, parent: QObject):
        super().__init__(QIcon(get_resource("quit.svg")), "&Quit", parent)
        self.setShortcut("Ctrl+Q")
        self.setStatusTip("Close NASM Debugger")
        self.triggered.connect(self.quit_app)

    @pyqtSlot()
    def quit_app(self):
        signals().exit_action_signal.emit()
