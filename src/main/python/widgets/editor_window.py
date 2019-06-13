from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QFrame


class EditorWindow(QFrame):
    """
    The editor window displays the currently opened file's contents if possible.
    Note that only a limited set of file types are supported.
    """
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QTextEdit())

        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setLayout(layout)
