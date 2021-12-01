# coding: utf-8

from logging import config
from .logging.configurations import STANDARD_CONSOLE_CONFIGURATION

# Configure the loggers
config.dictConfig(STANDARD_CONSOLE_CONFIGURATION)
