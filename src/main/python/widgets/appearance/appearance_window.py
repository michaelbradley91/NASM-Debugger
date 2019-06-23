from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QKeySequence
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QShortcut, QSplitter

from helpers.widget_helpers import centre_on_screen, size_from_percentage_of_screen
from service_locator import user_settings
from settings.user_settings import Key


class AppearanceWindow(QWidget):
    """
    This is the appearance window letting the user customise the appearance of the app.
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.Dialog)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Settings")
        self.resize(size_from_percentage_of_screen(0.7, 0.7))
        centre_on_screen(self)

        self.close_shortcut = QShortcut(QKeySequence("Esc"), self)
        # noinspection PyUnresolvedReferences
        self.close_shortcut.activated.connect(self.cancel_clicked)

        self.ok_button = QPushButton(self)
        self.ok_button.setText("OK")
        self.ok_button.clicked.connect(self.ok_clicked)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(self.cancel_clicked)

        self.apply_button = QPushButton(self)
        self.apply_button.setText("Apply")
        self.apply_button.clicked.connect(self.apply_clicked)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.ok_button)
        horizontal_layout.addWidget(self.cancel_button)
        horizontal_layout.addWidget(self.apply_button)

        self.vertical_splitter = QSplitter(Qt.Horizontal)
        self.vertical_splitter.setSizes([100000, 400000])

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.vertical_splitter)
        vertical_layout.addLayout(horizontal_layout)

        self.setLayout(vertical_layout)

        user_settings().restore_widget(self, Key.appearance)

    @pyqtSlot()
    def ok_clicked(self):
        self.close()

    @pyqtSlot()
    def cancel_clicked(self):
        self.close()

    @pyqtSlot()
    def apply_clicked(self):
        self.close()

    def closeEvent(self, event: QCloseEvent):
        user_settings().save_widget(self, Key.appearance)
        super().closeEvent(event)

