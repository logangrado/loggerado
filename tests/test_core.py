#!/usr/bin/env python3

import datetime
import logging
import io
import re

import pytest

from loggerado import configure_logger


@pytest.fixture
def logger():
    logger = logging.getLogger("test_logger")
    return logger


class TestCore:
    @pytest.mark.parametrize("level", [0, 1, 2, 3, 4])
    def test_basic(self, logger, level):
        stream = io.StringIO()
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        configure_logger(logger, levels[level], stream)

        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")

        nonce = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:") + r"\d{2}\.\d{3}"
        out = stream.getvalue().strip().split("\n")
        assert len(out) == len(levels) - level

        for i, level in enumerate(levels[level:]):
            message = out[i]
            print(message)
            expected = rf"\[{nonce}\] {level:>8s} | test_logger: {level.lower()}"
            assert re.match(expected, message)
