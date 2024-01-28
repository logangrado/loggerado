#!/usr/bin/env python3

import logging
import sys


def configure_logger(logger, level, stream=None):
    """Create a logging interface"""

    logger.propagate = False
    logger.handlers = []  # Remove all other handlers

    # Colors
    grey = "38;5;8"
    blue = "34"
    green = "32"
    yellow = "33"
    red = "31"

    if stream is None:
        stream = sys.stdout
    handler = logging.StreamHandler(stream=stream)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(levelname)8s | %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)
