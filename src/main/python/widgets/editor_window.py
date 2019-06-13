import codecs
import string
from typing import Optional

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTextEdit

from service_locator import signals
from widgets.helpers import ThinFrame, ThinVBoxLayout


class EditorWindow(ThinFrame):
    """
    The editor window displays the currently opened file's contents if possible.
    Note that only a limited set of file types are supported.
    """
    def __init__(self):
        super().__init__()

        self.editor = QTextEdit()
        self.current_file: Optional[str] = None

        layout = ThinVBoxLayout()
        layout.addWidget(self.editor)

        self.setLayout(layout)

        signals().file_selected_signal.connect(self.file_double_clicked)
        signals().folder_opened_signal.connect(self.folder_opened)

    @pyqtSlot(str)
    def file_double_clicked(self, path: str):
        # Show the contents of the file - skipping over binary if present
        with codecs.open(path, 'r', encoding='utf-8',
                         errors='ignore') as file:
            text = file.read()

        self.editor.setText(str.join("", (c for c in text if c in string.printable)))
        self.current_file = path

    @pyqtSlot()
    def folder_opened(self):
        # Deselect the current file
        self.current_file = None
        self.editor.setText("")
