"""
Entry point for running the application!
"""
import sys

from PyQt5.QtWidgets import QApplication
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from window import NASMDebuggerWindow


def set_styles(app: QApplication):
    app.setStyle("Fusion")


def run():
    application_context = ApplicationContext()

    set_styles(application_context.app)

    window = NASMDebuggerWindow(application_context.app)
    window.showMaximized()

    exit_code = application_context.app.exec()
    sys.exit(exit_code)


if __name__ == '__main__':
    run()
