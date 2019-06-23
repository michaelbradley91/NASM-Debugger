import os
from typing import Callable

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QDialog, QErrorMessage

from service_locator import get_resource, signals, user_settings
from settings.user_settings import Key, Default


class OpenAction(QAction):
    def __init__(self, parent: QObject):
        super().__init__(QIcon(get_resource("open_folder.svg")), "&Open Folder", parent)
        self.parent = parent
        self.setShortcut("Ctrl+O")
        self.setStatusTip("Open your project's folder.")
        self.triggered.connect(self.open_folder)

    def open_folder(self):
        """ Open a folder with the user's project files. """
        dialog = QFileDialog(self.parent, 'Select your project folder',
                             user_settings().get(Key.last_folder_opened, Default.last_folder_opened),
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
