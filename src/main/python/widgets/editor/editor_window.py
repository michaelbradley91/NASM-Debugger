import os
from typing import Optional, Dict

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QTabWidget

from service_locator import signals, user_settings
from settings.user_settings import Key
from widgets.common import ThinFrame, ThinVBoxLayout
from widgets.editor.editor_tab import EditorTab


class EditorWindow(ThinFrame):
    """
    The editor window displays the currently opened file's contents if possible.
    Note that only a limited set of file types are supported.
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.tabs = QTabWidget(self)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        # noinspection PyUnresolvedReferences
        self.tabs.tabCloseRequested.connect(self.tab_closing)

        layout = ThinVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        signals().file_selected_signal.connect(self.file_double_clicked)
        signals().folder_opened_signal.connect(self.folder_opened)

        # Mapping from file paths to tabs.
        self.open_files: Dict[str, EditorTab] = dict()

        # Restore from settings
        user_settings().restore_widget(self, Key.editor)
        for open_file_path in user_settings().get_from_json(Key.editor_open_files, []):
            self.add_file(open_file_path)
        self.select_file(user_settings().get(Key.editor_current_file))

    @pyqtSlot(int)
    def tab_closing(self, index: int):
        # Remove the tab from the mapping
        tab = self.tabs.widget(index)
        self.close_tab(tab)

    def get_path_by_tab(self, tab: QWidget) -> Optional[str]:
        """ Get a path by the tab. """
        for path, saved_tab in self.open_files.items():
            if saved_tab == tab:
                return path
        return None

    @pyqtSlot(str)
    def file_double_clicked(self, path: str):
        """
        Add a new tab with the contents of the file if it has not been shown.
        Always select the tab for this file.
        """
        self.add_file(path)
        self.select_file(path)

    def select_file(self, path: str):
        """ Select a file by the file path. """
        if path in self.open_files:
            tab = self.open_files[path]
            index = self.tabs.indexOf(tab)
            self.tabs.setCurrentIndex(index)

    def add_file(self, path: str):
        """ Add a new file to the tabs. """
        if path not in self.open_files and os.path.isfile(path):
            tab = EditorTab(path, self)
            self.tabs.addTab(tab, os.path.basename(path))
            self.open_files[path] = tab

    @pyqtSlot()
    def folder_opened(self):
        # Close all tabs.
        for tab in list(self.open_files.values()):
            self.close_tab(tab)
        self.open_files.clear()

    def close_tab(self, tab: QWidget):
        # Cleanly remove a tab
        index = self.tabs.indexOf(tab)
        path = self.get_path_by_tab(tab)
        if path:
            self.open_files.pop(path)
        tab.deleteLater()
        self.tabs.removeTab(index)

    def closeEvent(self, event: QCloseEvent):
        user_settings().save_widget(self, Key.editor)
        user_settings().save_as_json(Key.editor_open_files, list(self.open_files.keys()))

        current_index = self.tabs.currentIndex()
        if current_index >= 0:
            tab: EditorTab = self.tabs.widget(current_index)
            user_settings().save(Key.editor_current_file, tab.path)

        for tab in self.open_files.values():
            tab.close()

        super().closeEvent(event)
