from PyQt5.QtWidgets import QWidget, QTextEdit

from helpers.file_helpers import read_file_text
from widgets.common import ThinVBoxLayout
from widgets.editor.code_editor import CodeEditor


class EditorTab(QWidget):
    """ A single file tab in the editor window. """
    def __init__(self, path: str, parent: QWidget):
        super().__init__(parent)

        self.editor = CodeEditor(self)
        self.editor.setPlainText(read_file_text(path))

        layout = ThinVBoxLayout()
        layout.addWidget(self.editor)

        self.setLayout(layout)