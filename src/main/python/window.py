"""
The top level window
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QSplitter
from injector import inject

from menu import Menu
from service_locator import signals
from settings.user_settings import UserSettings, Key
from widgets.editor.editor_window import EditorWindow
from widgets.project.project_window import ProjectWindow
from widgets.tools_window import ToolsWindow


class NASMDebuggerWindow(QMainWindow):
    """ The top level window for the NASM debugger. """
    @inject
    def __init__(self, app: QApplication, user_settings: UserSettings):
        super().__init__()
        self.app = app
        self.user_settings = user_settings

        # Connect to signals
        signals().exit_action_signal.connect(self.exit_app)

        self.project = ProjectWindow(self)
        self.editor = EditorWindow(self)
        self.tools = ToolsWindow(self)
        self.setCentralWidget(self.editor)
        self.setContentsMargins(0, 0, 0, 0)
        self.resize(800, 500)
        self.setWindowTitle(app.applicationDisplayName())

        self.statusBar().showMessage(f"Welcome to {app.applicationDisplayName()}!")

        # Create the menu
        self.menu = Menu(self)

        # Split the window
        self.horizontal_splitter = QSplitter(Qt.Horizontal)
        self.horizontal_splitter.addWidget(self.project)
        self.horizontal_splitter.addWidget(self.editor)
        self.horizontal_splitter.setSizes([100000, 500000])

        self.vertical_splitter = QSplitter(Qt.Vertical)
        self.vertical_splitter.addWidget(self.horizontal_splitter)
        self.vertical_splitter.addWidget(self.tools)
        self.vertical_splitter.setSizes([250000, 100000])

        self.setCentralWidget(self.vertical_splitter)

        self.user_settings.restore_widget(self, Key.window)
        self.user_settings.restore_widget(self.horizontal_splitter, Key.window_horizontal_splitter)
        self.user_settings.restore_widget(self.vertical_splitter, Key.window_vertical_splitter)

    def closeEvent(self, event: QCloseEvent):
        # Clear all settings keys to ensure we don't leave old settings behind
        self.user_settings.clear()
        self.user_settings.save_widget(self, Key.window)
        self.user_settings.save_widget(self.horizontal_splitter, Key.window_horizontal_splitter)
        self.user_settings.save_widget(self.vertical_splitter, Key.window_vertical_splitter)
        self.project.close()
        self.editor.close()
        self.tools.close()
        super().closeEvent(event)

    def exit_app(self):
        self.close()
        self.app.exit()
