import os
import pickle
from typing import List

from PyQt5.QtCore import QDir, pyqtSlot, QModelIndex
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QTreeView, QWidget, QFileSystemModel

from service_locator import signals, user_settings
from settings.user_settings import Key, Default


class ProjectTreeView(QTreeView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.doubleClicked.connect(self.file_or_directory_double_clicked)
        signals().folder_opened_signal.connect(self.folder_opened)

        self.file_system_model = QFileSystemModel(self)
        # noinspection PyUnresolvedReferences
        self.file_system_model.directoryLoaded.connect(self.directory_loaded)
        self.file_system_model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        self.setModel(self.file_system_model)

        self.setHeaderHidden(True)
        # Hide all but the name column of the tree view.
        for i in range(1, self.file_system_model.columnCount()):
            self.hideColumn(i)

        self.set_path(user_settings().get(Key.last_folder_opened, Default.last_folder_opened))
        self.loading_previous_folder = True

    def set_path(self, path: str):
        """ Change the path of the project window. """
        self.loading_previous_folder = False  # Do not try to reload the previous user's settings on this new folder.
        self.file_system_model.setRootPath(path)
        # This shows the selected path's contents rather than the path itself.
        self.setRootIndex(self.file_system_model.index(path))
        self.clearSelection()

    # noinspection PyUnusedLocal
    @pyqtSlot(str)
    def directory_loaded(self, path):
        # We have to restore the tree view here to ensure it is expanded
        # only when the directory is ready to be searched.
        if self.loading_previous_folder:
            user_settings().restore_widget(self, Key.project_tree)
            self.loading_previous_folder = False

    @pyqtSlot(QModelIndex)
    def file_or_directory_double_clicked(self, index: QModelIndex):
        """ Send a signal so we can react to the user's double click on a file in the project view. """
        path = self.file_system_model.filePath(index)
        if path and os.path.isfile(path):
            signals().file_selected_signal.emit(path)

    @pyqtSlot(str)
    def folder_opened(self, folder: str):
        self.set_path(folder)
        user_settings().save(Key.last_folder_opened, folder)

    # noinspection PyPep8Naming
    def saveState(self):
        is_expanded: List[str] = []
        for index in self.file_system_model.persistentIndexList():
            if self.isExpanded(index):
                is_expanded.append(self.file_system_model.filePath(index))
        return pickle.dumps(is_expanded)

    # noinspection PyPep8Naming
    def restoreState(self, is_expanded: bytes):
        is_expanded_list = pickle.loads(is_expanded)
        self.setUpdatesEnabled(False)
        for path in is_expanded_list:
            if os.path.isdir(path):
                index = self.file_system_model.index(path)
                self.setExpanded(index, True)
        self.setUpdatesEnabled(True)

    def closeEvent(self, event: QCloseEvent):
        user_settings().save_widget(self, Key.project_tree)
        super().closeEvent(event)
