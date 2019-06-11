import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QTextEdit
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
from pyqode.qt import QtWidgets

def on_top_clicked():
    alert = QMessageBox()
    alert.setText("You clicked the button!")
    alert.exec()


if __name__ == '__main__':
    application_context = ApplicationContext()       # 1. Instantiate ApplicationContext
    app = application_context.app

    main_window = QMainWindow()
    main_window.resize(400, 150)

    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ButtonText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QPushButton { margin: 1ex; padding: 1ex }")

    editor = api.CodeEdit()
    # start the backend as soon as possible
    editor.backend.start('code-editor-server.py')

    # append some modes and panels
    editor.modes.append(modes.CodeCompletionMode())
    editor.modes.append(modes.PygmentsSyntaxHighlighter(editor.document()))
    editor.modes.append(modes.CaretLineHighlighterMode())
    editor.panels.append(panels.SearchAndReplacePanel(),
                         api.Panel.Position.BOTTOM)

    # open a file
    editor.file.open("example.txt")

    main_window.setCentralWidget(editor)
    main_window.show()

    exit_code = app.exec()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
