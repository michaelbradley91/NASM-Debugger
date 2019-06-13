"""
Entry point for running the application!
"""
import sys
import service_locator

from injector import Injector
from PyQt5.QtWidgets import QApplication
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from injector_module import InjectionModule
from window import NASMDebuggerWindow


def set_styles(app: QApplication):
    pass


def run():
    application_context = ApplicationContext()
    set_styles(application_context.app)

    service_locator.set_injector(Injector([InjectionModule(application_context)]))
    logger = service_locator.logger()
    logger.info("Welcome to NASM Debugger! The application is starting up...")
    logger.info(f"Log files are written to {service_locator.config().logs_directory}")
    logger.info(f"Settings are taken from {service_locator.config().settings_directory}")

    window = service_locator.get_service(NASMDebuggerWindow)
    window.showMaximized()

    exit_code = application_context.app.exec()
    sys.exit(exit_code)


if __name__ == '__main__':
    run()
