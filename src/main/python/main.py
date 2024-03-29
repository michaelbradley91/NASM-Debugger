"""
Entry point for running the application!
"""
import sys

from PyQt5.QtWidgets import QApplication
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from injector import Injector

import service_locator
from injector_module import InjectionModule
from window import NASMDebuggerWindow


def run():
    application_context = ApplicationContext()

    service_locator.set_injector(Injector([InjectionModule(application_context)]))
    app: QApplication = application_context.app
    app.setApplicationDisplayName("NASM Debugger")
    app.setOrganizationName("personal")
    app.setOrganizationDomain("com.michael.bradley.nasm-debugger")
    app.setQuitOnLastWindowClosed(True)
    # noinspection PyUnresolvedReferences
    app.lastWindowClosed.connect(save_settings)

    logger = service_locator.logger()
    logger.info("Welcome to NASM Debugger! The application is starting up...")
    logger.info(f"Log files are written to {service_locator.config().logs_directory}")
    logger.info(f"User settings are written to {service_locator.settings().user.file_path()}")

    window = service_locator.get_service(NASMDebuggerWindow)
    window.show()

    exit_code = application_context.app.exec()
    sys.exit(exit_code)


def save_settings():
    settings = service_locator.settings()
    settings.user.sync()

if __name__ == '__main__':
    run()
