"""
The top level window
"""
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication, QSplitter, QWidget, QHBoxLayout, QFileSystemModel, \
    QTreeView, QFrame
from injector import inject

from actions.quit_action import QuitAction
from widgets.editor_window import EditorWindow
from widgets.project_window import ProjectWindow
from widgets.tools_window import ToolsWindow


class NASMDebuggerWindow(QMainWindow):
    """ The top level window for the NASM debugger. """
    @inject
    def __init__(self, app: QApplication, project: ProjectWindow, editor: EditorWindow, tools: ToolsWindow):
        super().__init__()
        self.app = app
        self.project = project
        self.editor = editor
        self.tools = tools
        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)
        self.setWindowTitle("NASM Debugger")

        self.statusBar().showMessage("Welcome to NASM Debugger!")

        # Create the menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('&File')
        self.file_menu.addAction(QuitAction(self.app.exit, self))

        # Split the window
        horizontal_splitter = QSplitter(Qt.Horizontal)
        horizontal_splitter.addWidget(project)
        horizontal_splitter.addWidget(editor)
        horizontal_splitter.setSizes([100000, 500000])

        vertical_splitter = QSplitter(Qt.Vertical)
        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.addWidget(tools)
        vertical_splitter.setSizes([250000, 100000])

        self.setCentralWidget(vertical_splitter)
