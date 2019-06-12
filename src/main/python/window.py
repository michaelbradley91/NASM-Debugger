"""
The top level window
"""
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication

from actions.quit_action import QuitAction


class NASMDebuggerWindow(QMainWindow):
    """ The top level window for the NASM debugger. """

    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)
        self.setWindowTitle("NASM Debugger")

        self.statusBar().showMessage("Welcome to NASM Debugger!")

        # Create the menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('&File')
        self.file_menu.addAction(QuitAction(self.app.exit, self))
