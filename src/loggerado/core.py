#!/usr/bin/env python3

import logging
import sys


def colorize(string, codes):
    if not isinstance(codes, str):
        codes = ";".join(codes)
    code = "\033[" + codes + "m"

    return f"{code}{string}\033[0m"


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def __init__(self, ansi=True):
        self._ansi = ansi

        # Colors
        grey = "38;5;8"
        blue = "34"
        green = "32"
        yellow = "33"
        red = "31"

        self._timestamp = "%(asctime)s.%(msecs)03d"
        self._levelname = "%(levelname)8s"
        self._name = "%(name)s"
        self._message = "%(message)s"
        self._datefmt = "%Y-%m-%d %H:%M:%S"

        # Non-ansi format
        self._format = f"[{self._timestamp}] {self._levelname} | {self._name}: {self._message}"

        # Ansi formats
        self._ansi_formats = {
            logging.DEBUG: self._get_format(grey, blue, grey),
            logging.INFO: self._get_format(grey, green, grey),
            logging.WARNING: self._get_format(grey, yellow, grey),
            logging.ERROR: self._get_format(grey, red, grey),
            logging.CRITICAL: self._get_format(grey, red, grey),
        }

    def _get_format(self, time_color, level_color, name_color):
        return f"{colorize(self._timestamp, time_color)} {colorize(self._levelname, level_color)} {colorize(self._name,name_color)} {self._message}"

    def format(self, record):
        if self._ansi:
            log_fmt = self._ansi_formats.get(record.levelno)
        else:
            log_fmt = self._format

        formatter = logging.Formatter(log_fmt, datefmt=self._datefmt)
        return formatter.format(record)


def configure_logger(logger, level, stream=None, ansi=False):
    """Create a logging interface"""

    logger.propagate = False
    logger.handlers = []  # Remove all other handlers

    if stream is None:
        stream = sys.stdout
    handler = logging.StreamHandler(stream=stream)

    # create formatter and add it to the handlers
    formatter = CustomFormatter(ansi=ansi)

    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)
