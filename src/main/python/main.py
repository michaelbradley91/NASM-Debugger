import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QMainWindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext


def on_top_clicked():
    alert = QMessageBox()
    alert.setText("You clicked the button!")
    alert.exec()


if __name__ == '__main__':
    application_context = ApplicationContext()       # 1. Instantiate ApplicationContext
    app = application_context.app

    main_window = QMainWindow()
    main_window.resize(400, 150)

    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ButtonText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QPushButton { margin: 1ex; padding: 1ex }")

    window = QWidget()
    layout = QVBoxLayout()
    button = QPushButton('Top')
    button.clicked.connect(on_top_clicked)
    layout.addWidget(button)
    layout.addWidget(QPushButton('Bottom'))
    window.setLayout(layout)
    main_window.setCentralWidget(window)
    main_window.show()

    exit_code = app.exec()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
