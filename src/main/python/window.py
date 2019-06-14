"""
The top level window
"""
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication, QSplitter, QFileDialog, QDialog, QErrorMessage
from injector import inject

from actions.open_action import OpenAction
from actions.quit_action import QuitAction
from service_locator import signals
from widgets.editor.editor_window import EditorWindow
from widgets.project_window import ProjectWindow
from widgets.tools_window import ToolsWindow


class NASMDebuggerWindow(QMainWindow):
    """ The top level window for the NASM debugger. """
    @inject
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.project = ProjectWindow(self)
        self.editor = EditorWindow(self)
        self.tools = ToolsWindow(self)
        self.setCentralWidget(self.editor)
        self.resize(800, 500)
        self.setWindowTitle("NASM Debugger")
        self.setContentsMargins(0, 0, 0, 0)

        self.statusBar().showMessage("Welcome to NASM Debugger!")

        # Create the menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('&File')
        self.file_menu.addAction(OpenAction(self.open_folder, self))
        self.file_menu.addAction(QuitAction(self.app.exit, self))

        # Split the window
        horizontal_splitter = QSplitter(Qt.Horizontal)
        horizontal_splitter.addWidget(self.project)
        horizontal_splitter.addWidget(self.editor)
        horizontal_splitter.setSizes([100000, 500000])

        vertical_splitter = QSplitter(Qt.Vertical)
        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.addWidget(self.tools)
        vertical_splitter.setSizes([250000, 100000])

        self.setCentralWidget(vertical_splitter)

    def open_folder(self):
        """ Open a folder with the user's project files. """
        dialog = QFileDialog(self, 'Select your project folder', os.path.expanduser('~'),
                             "Assembly (*.asm);;All files (*)")
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec() == QDialog.Accepted:
            # Check a directory really was chosen as this is reliant on the system dialog
            if not dialog.selectedFiles():
                QErrorMessage().showMessage("Please select only a folder to open.")
                return

            chosen_directory = dialog.selectedFiles()[0]
            if not os.path.isdir(chosen_directory):
                QErrorMessage().showMessage("Please select only a folder to open.")
                return

            signals().folder_opened_signal.emit(chosen_directory)
