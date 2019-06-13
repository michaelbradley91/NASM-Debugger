import os

from PyQt5.QtCore import QDir, pyqtSlot, QModelIndex
from PyQt5.QtWidgets import QFileSystemModel, QTreeView

from service_locator import signals
from widgets.helpers import ThinVBoxLayout, ThinFrame


class ProjectWindow(ThinFrame):
    """
    The project window shows the files available in the file system which the user opened.
    The user can select files to show them in the editor window.
    """
    def __init__(self):
        super().__init__()

        path = "/"
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(path)
        self.file_system_model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        tree_view = QTreeView()
        tree_view.setHeaderHidden(True)
        tree_view.setModel(self.file_system_model)
        tree_view.doubleClicked.connect(self.file_or_directory_double_clicked)

        # Hide all but the name column of the tree view.
        for i in range(1, self.file_system_model.columnCount()):
            tree_view.hideColumn(i)

        # This shows the selected path's contents rather than the path itself.
        tree_view.setRootIndex(self.file_system_model.index(path))

        layout = ThinVBoxLayout()
        layout.addWidget(tree_view)
        self.setLayout(layout)

    @pyqtSlot(QModelIndex)
    def file_or_directory_double_clicked(self, index: QModelIndex):
        """ Send a signal so we can react to the user's double click on a file in the project view. """
        path = self.file_system_model.filePath(index)
        if os.path.isfile(path):
            signals().file_selected_signal.emit(path)
