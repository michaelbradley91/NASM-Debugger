from PyQt5.QtWidgets import QTextEdit

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
