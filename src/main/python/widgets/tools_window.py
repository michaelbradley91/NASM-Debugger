from PyQt5.QtWidgets import QFrame, QWidget

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
