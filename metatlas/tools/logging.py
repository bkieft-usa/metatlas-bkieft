"""
Logging configuration for Metatlas

based on https://gist.github.com/joshbode/58fac7ababc700f51e2a9ecdebe563ad

Usage:
import logging
from metatlas.tools.logging import activate_logging

logger = logging.getLogger('metatlas.jupyter')
activate_logging()
"""

import getpass
import os
import sys
import logging
from typing import Optional, Dict

from colorama import Fore, Back, Style

levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""

    def __init__(self, *args, colors: Optional[Dict[str, str]] = None, **kwargs) -> None:
        """Initialize the formatter with specified format strings."""

        super().__init__(*args, **kwargs)

        self.colors = colors if colors else {}

    def format(self, record) -> str:
        """Format the specified record as text."""

        record.color = self.colors.get(record.levelname, "")
        record.reset = Style.RESET_ALL

        return super().format(record)


def activate_module_logging(
    module, console_level="INFO", console_format=None, file_level="DEBUG", filename=None
):
    """
    inputs:
        module: name of logger to capture messages from, often a module name
        console_level: string with desired logging level for messages on stdout (notebook)
        file_level: string with desired logging level for message to log file
        filename: file to send logs to
    returns logger

    Call this function to activate logging to console and file
    valid logging levels are 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    """
    console_handler = get_console_handler(console_level, console_format)
    file_handler = get_file_handler(file_level, filename)

    logger = logging.getLogger(module)
    logger.handlers[:] = []
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(
        levels[file_level] if levels[file_level] < levels[console_level] else levels[console_level]
    )
    return logger


def disable_jupyter_default_logging():
    """
    stop jupyter from making its own root-level logger
     note that jupyter delays creating the root-level logger until a log message is generated
    """
    jupyter_logger = logging.getLogger()
    jupyter_logger.handlers[:] = []
    jupyter_logger.addHandler(logging.NullHandler())


def get_file_handler(level, filename=None):
    """
    inputs:
        level: one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        filename: logging destination
    Returns a logging.FileHandler object
    """
    if filename is None:
        if "METATLAS_LOCAL" in os.environ:
            filename = "metatlas.log"
        else:
            filename = f"/global/cfs/projectdirs/m2650/jupyter_logs/{getpass.getuser()}.log"
    file_formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(name)s;%(message)s")
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(levels[level])
    return file_handler


def get_console_handler(level, format_str=None):
    """
    inputs:
        level: one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        format_str: input to logging.setFormatter
    Returns a logging.StreamHandler object
    """
    if format_str is None:
        format_str = "{asctime} {color}{levelname:8}{reset} {message}"
    console_formatter = ColoredFormatter(
        format_str,
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        colors={
            "DEBUG": Fore.CYAN,
            "INFO": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "CRITICAL": Fore.WHITE + Back.RED,
        },
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(levels[level])
    return console_handler


def activate_logging(console_level="INFO", console_format=None, file_level="DEBUG", filename=None):
    """
    inputs:
        console_level: string with desired logging level for messages on stdout (notebook)
        file_level: string with desired logging level for message to log file
        filename: file to send logs to
    returns logger

    Call this function to activate logging to console and file
    valid logging levels are 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    """
    disable_jupyter_default_logging()
    activate_module_logging("metatlas", console_level, console_format, file_level, filename)
