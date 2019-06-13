from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QFrame

from widgets.helpers import ThinVBoxLayout, ThinFrame


class ProjectWindow(ThinFrame):
    """
    The project window shows the files available in the file system which the user opened.
    The user can select files to show them in the editor window.
    """
    def __init__(self):
        super().__init__()

        path = "/"
        file_system = QFileSystemModel()
        file_system.setRootPath(path)
        file_system.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        tree_view = QTreeView()
        tree_view.setHeaderHidden(True)
        tree_view.setModel(file_system)

        # Hide all but the name column of the tree view.
        for i in range(1, file_system.columnCount()):
            tree_view.hideColumn(i)

        # This shows the selected path's contents rather than the path itself.
        tree_view.setRootIndex(file_system.index(path))

        layout = ThinVBoxLayout()
        layout.addWidget(tree_view)
        self.setLayout(layout)
