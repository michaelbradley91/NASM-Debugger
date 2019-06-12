import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QTextEdit
from fbs_runtime.application_context.PyQt5 import ApplicationContext

def on_top_clicked():
    alert = QMessageBox()
    alert.setText("You clicked the button!")
    alert.exec()


if __name__ == '__main__':
    application_context = ApplicationContext()
    app = application_context.app

    main_window = QMainWindow()
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ButtonText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QPushButton { margin: 1ex; padding: 1ex }")

    editor = QTextEdit()
    main_window.setCentralWidget(editor)
    main_window.showMaximized()

    exit_code = app.exec()
    sys.exit(exit_code)
