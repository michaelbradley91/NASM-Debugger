from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QTextEdit

from helpers.file_helpers import read_file_text
from helpers.helpers import to_base64
from service_locator import user_settings
from settings.user_settings import Key
from widgets.common import ThinVBoxLayout
from widgets.editor.code_editor import CodeEditor
from widgets.syntax_highlighters.nasm_highlighter import NASMHighlighter


class EditorTab(QWidget):
    """ A single file tab in the editor window. """
    def __init__(self, path: str, parent: QWidget):
        super().__init__(parent)
        self.path = path
        self.settings_key = Key.editor_tab.value + to_base64(path)
        self.editor = CodeEditor(self)
        self.highlighter = NASMHighlighter(self.editor.document())
        self.editor.setPlainText(read_file_text(path))

        layout = ThinVBoxLayout()
        layout.addWidget(self.editor)

        self.setLayout(layout)

        user_settings().restore_widget(self, self.settings_key)

    def closeEvent(self, event: QCloseEvent):
        user_settings().save_widget(self, self.settings_key)
        super().closeEvent(event)
