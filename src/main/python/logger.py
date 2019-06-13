import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

from injector import inject

from configuration import Configuration


class LevelFilter(logging.Filter):
    """ A simple filter based on log levels. """
    def __init__(self, *, low: Optional[int] = None, high: Optional[int] = None):
        """ Creating a logging filter. The high end is exclusive, and the low end is inclusive. """
        super().__init__()
        self.low = low
        self.high = high

    def filter(self, record):
        if self.low and record.levelno < self.low:
            return False
        if self.high and record.levelno >= self.high:
            return False
        return True


@inject
def create_logger(config: Configuration):
    """ Create the application's logger. """
    logger = logging.getLogger(config.path_safe_app_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Create handlers
    standard_out_handler = logging.StreamHandler(sys.stdout)
    standard_error_handler = logging.StreamHandler(sys.stderr)
    standard_out_handler.addFilter(LevelFilter(high=logging.ERROR))
    standard_error_handler.addFilter(LevelFilter(low=logging.ERROR))
    standard_out_handler.setFormatter(formatter)
    standard_error_handler.setFormatter(formatter)

    debug_log_file_name = os.path.join(config.logs_directory, "debug")
    error_log_file_name = os.path.join(config.logs_directory, "error")
    debug_file_handler = RotatingFileHandler(debug_log_file_name, mode='a', maxBytes=5*1024*1024,
                                             backupCount=2, encoding=None, delay=0)
    error_file_handler = RotatingFileHandler(error_log_file_name, mode='a', maxBytes=5*1024*1024,
                                             backupCount=2, encoding=None, delay=0)
    debug_file_handler.addFilter(LevelFilter(low=logging.DEBUG))
    error_file_handler.addFilter(LevelFilter(low=logging.WARNING)) # Warnings may be useful when diagnosing an error.
    debug_file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(standard_out_handler)
    logger.addHandler(standard_error_handler)
    logger.addHandler(debug_file_handler)
    logger.addHandler(error_file_handler)

    return logger
