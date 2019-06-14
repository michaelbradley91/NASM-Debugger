import os

from PyQt5.QtCore import QDir, pyqtSlot, QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QWidget

from service_locator import signals
from widgets.common import ThinVBoxLayout, ThinFrame


class ProjectWindow(ThinFrame):
    """
    The project window shows the files available in the file system which the user opened.
    The user can select files to show them in the editor window.
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.file_system_model = QFileSystemModel(self)
       
        self.file_system_model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        self.tree_view = QTreeView(self)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.doubleClicked.connect(self.file_or_directory_double_clicked)

        # Hide all but the name column of the tree view.
        for i in range(1, self.file_system_model.columnCount()):
            self.tree_view.hideColumn(i)

        # TODO set this back to the user's home directory, but remember where we left off!
        # self.set_path(os.path.expanduser("~"))
        self.set_path(os.path.join("/", "app", "assembly"))

        layout = ThinVBoxLayout()
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        signals().folder_opened_signal.connect(self.folder_opened)
        
    def set_path(self, path: str):
        """ Change the path of the project window. """
        self.file_system_model.setRootPath(path)
        # This shows the selected path's contents rather than the path itself.
        self.tree_view.setRootIndex(self.file_system_model.index(path))
        self.tree_view.clearSelection()

    @pyqtSlot(QModelIndex)
    def file_or_directory_double_clicked(self, index: QModelIndex):
        """ Send a signal so we can react to the user's double click on a file in the project view. """
        path = self.file_system_model.filePath(index)
        if path and os.path.isfile(path):
            signals().file_selected_signal.emit(path)

    @pyqtSlot(str)
    def folder_opened(self, folder: str):
        self.set_path(folder)
