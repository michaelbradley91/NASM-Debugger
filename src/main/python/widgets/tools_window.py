from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QFrame, QWidget

from service_locator import user_settings
from settings.user_settings import Key
from widgets.common import ThinFrame, ThinVBoxLayout


class ToolsWindow(ThinFrame):
    """
    The tools window shows various tools that can help with running and debugging
    the program.
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)

        layout = ThinVBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

        user_settings().restore_widget(self, Key.tools)

    def closeEvent(self, event: QCloseEvent):
        user_settings().save_widget(self, Key.tools)
        super().closeEvent(event)
