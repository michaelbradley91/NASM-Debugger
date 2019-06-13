from logging import Logger

from PyQt5.QtWidgets import QApplication
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from injector import Module, singleton, provider

from configuration import Configuration
from logger import create_logger
from widgets.editor_window import EditorWindow
from widgets.project_window import ProjectWindow
from widgets.tools_window import ToolsWindow
from window import NASMDebuggerWindow


class InjectionModule(Module):
    def __init__(self, application_context: ApplicationContext):
        self.application_context: ApplicationContext = application_context

    def configure(self, binder):
        binder.bind(ApplicationContext, to=self.application_context, scope=singleton)
        binder.bind(QApplication, to=self.application_context.app, scope=singleton)

        binder.bind(NASMDebuggerWindow)
        binder.bind(ProjectWindow)
        binder.bind(EditorWindow)
        binder.bind(ToolsWindow)

        binder.bind(Configuration, scope=singleton)
        binder.bind(Logger, to=create_logger, scope=singleton)
