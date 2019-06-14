from PyQt5.QtWidgets import QWidget, QTextEdit

from helpers.file_helpers import read_file_text
from widgets.common import ThinVBoxLayout
from widgets.editor.code_editor import CodeEditor
from widgets.syntax_highlighters.nasm_highlighter import NASMHighlighter


class EditorTab(QWidget):
    """ A single file tab in the editor window. """
    def __init__(self, path: str, parent: QWidget):
        super().__init__(parent)

        self.editor = CodeEditor(self)
        self.highlighter = NASMHighlighter(self.editor.document())
        self.editor.setPlainText(read_file_text(path))

        layout = ThinVBoxLayout()
        layout.addWidget(self.editor)

        self.setLayout(layout)