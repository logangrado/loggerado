#!/usr/bin/env python3

from typing import Optional, IO
import logging
import sys


def _colorize(string, codes):
    if not isinstance(codes, str):
        codes = ";".join(codes)
    code = "\033[" + codes + "m"

    return f"{code}{string}\033[0m"


class CustomFormatter(logging.Formatter):
    def __init__(self, ansi=True, use_base_name=False):
        self._ansi = ansi
        self._use_base_name = use_base_name

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
        return " ".join(
            [
                _colorize(self._timestamp, time_color),
                _colorize(self._levelname, level_color),
                _colorize(self._name, name_color),
                self._message,
            ]
        )

    def format(self, record):
        if self._ansi:
            log_fmt = self._ansi_formats.get(record.levelno)
        else:
            log_fmt = self._format

        if self._use_base_name:
            record.name = record.name.split(".")[0]

        formatter = logging.Formatter(log_fmt, datefmt=self._datefmt)
        return formatter.format(record)


def configure_logger(
    logger: logging.Logger,
    level: str,
    stream: Optional[IO[str]] = None,
    ansi: bool = False,
    use_base_name: bool = False,
) -> None:
    """
    Configure logger

    Parameters
    ----------
    logger
        Logger to configure
    level
        Logging level to set
    stream
        Logging output stream. If None, defaults to sys.stdout
    ansi
        If True, use Ansi characters
    use_base_name
        If True, only use the logger's base name (e.g. `logger` vs `logger.module`, etc)
    """

    logger.propagate = False
    logger.handlers = []  # Remove all other handlers

    if stream is None:
        stream = sys.stdout
    handler = logging.StreamHandler(stream=stream)

    # Create formatter and add it to the handlers
    formatter = CustomFormatter(ansi=ansi, use_base_name=use_base_name)

    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)
