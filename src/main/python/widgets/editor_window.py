from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTextEdit

from service_locator import signals, logger
from widgets.helpers import ThinFrame, ThinVBoxLayout


class EditorWindow(ThinFrame):
    """
    The editor window displays the currently opened file's contents if possible.
    Note that only a limited set of file types are supported.
    """
    def __init__(self):
        super().__init__()

        layout = ThinVBoxLayout()
        layout.addWidget(QTextEdit())

        self.setLayout(layout)

        signals().file_selected_signal.connect(self.file_double_clicked)

    @pyqtSlot(str)
    def file_double_clicked(self, path: str):
        logger().info(f"File double clicked! {path}")
