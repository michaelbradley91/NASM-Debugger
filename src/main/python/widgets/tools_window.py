from PyQt5.QtWidgets import QVBoxLayout, QFrame


class ToolsWindow(QFrame):
    """
    The tools window shows various tools that can help with running and debugging
    the program.
    """
    def __init__(self):
        super().__init__()

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)

        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLayout(layout)
