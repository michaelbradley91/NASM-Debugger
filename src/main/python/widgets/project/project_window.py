from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget

from service_locator import user_settings
from settings.user_settings import Key
from widgets.common import ThinVBoxLayout, ThinFrame
from widgets.project.project_tree_view import ProjectTreeView


class ProjectWindow(ThinFrame):
    """
    The project window shows the files available in the file system which the user opened.
    The user can select files to show them in the editor window.
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.tree_view = ProjectTreeView(self)

        layout = ThinVBoxLayout()
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        user_settings().restore_widget(self, Key.project)

    def closeEvent(self, event: QCloseEvent):
        user_settings().save_widget(self, Key.project)
        self.tree_view.close()
        super().closeEvent(event)
