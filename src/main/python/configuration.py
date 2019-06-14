import os

import appdirs
from PyQt5.QtWidgets import QApplication
from injector import inject


class Configuration:
    """ Root class of application specific configuration """
    @inject
    def __init__(self, app: QApplication):
        self.app = app
        # Initialise directories
        try:
            os.makedirs(self.logs_directory)
        except FileExistsError:
            pass
        try:
            os.makedirs(self.user_settings_directory)
        except FileExistsError:
            pass

    @property
    def app_name(self) -> str:
        return self.app.applicationDisplayName()

    @property
    def path_safe_app_name(self) -> str:
        return self.app_name.replace(" ", "_").lower()

    @property
    def app_author(self) -> str:
        return self.app.organizationName()

    @property
    def path_safe_app_author(self) -> str:
        return self.app_author.replace(" ", "_").lower()

    @property
    def app_version(self) -> str:
        return "0.0.0"

    @property
    def logs_directory(self) -> str:
        return appdirs.user_log_dir(self.path_safe_app_name, self.path_safe_app_author, self.app_version)

    @property
    def user_settings_directory(self) -> str:
        return appdirs.user_config_dir(self.path_safe_app_name, self.path_safe_app_author)
