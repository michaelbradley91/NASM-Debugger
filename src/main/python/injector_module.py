from logging import Logger

from PyQt5.QtWidgets import QApplication
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from injector import Module, singleton, Binder

from configuration import Configuration
from logger import create_logger
from settings.settings import Settings
from settings.user_settings import UserSettings
from signals import Signals


class InjectionModule(Module):
    """
    Configures dependency injection throughout the application.
    """
    def __init__(self, application_context: ApplicationContext):
        self.application_context: ApplicationContext = application_context

    def configure(self, binder: Binder):
        binder.bind(ApplicationContext, to=self.application_context, scope=singleton)
        binder.bind(QApplication, to=self.application_context.app, scope=singleton)
        binder.bind(Configuration, scope=singleton)
        binder.bind(Logger, to=create_logger, scope=singleton)
        binder.bind(Signals, scope=singleton)
        binder.bind(Settings, scope=singleton)
        binder.bind(UserSettings, scope=singleton)
