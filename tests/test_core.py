#!/usr/bin/env python3

import datetime
import logging
import io
import re

import pytest
import freezegun

from loggerado import configure_logger


@pytest.fixture
def logger():
    logger = logging.getLogger("test_logger.logger")
    return logger


@freezegun.freeze_time("2001-01-01", tz_offset=0)
class TestCore:
    @pytest.mark.parametrize("level", [0, 1, 2, 3, 4])
    def test_basic(self, logger, level):
        stream = io.StringIO()
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        expected = [
            "[2000-12-31 18:00:00.000] CRITICAL | test_logger.logger: critical",
            "[2000-12-31 18:00:00.000]    ERROR | test_logger.logger: error",
            "[2000-12-31 18:00:00.000]  WARNING | test_logger.logger: warning",
            "[2000-12-31 18:00:00.000]     INFO | test_logger.logger: info",
            "[2000-12-31 18:00:00.000]    DEBUG | test_logger.logger: debug",
        ]

        configure_logger(logger, levels[level], stream)

        logger.critical("critical")
        logger.error("error")
        logger.warning("warning")
        logger.info("info")
        logger.debug("debug")

        out = stream.getvalue().strip().split("\n")

        assert len(out) == len(levels) - level

        for i, level in enumerate(levels[level:]):
            message = out[i]
            print(message)
            assert message == expected[i]

    @pytest.mark.parametrize("level", [0, 1, 2, 3, 4])
    def test_ansi(self, logger, level):
        stream = io.StringIO()
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        expected = [
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[31mCRITICAL\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m critical",
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[31m   ERROR\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m error",
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[33m WARNING\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m warning",
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[32m    INFO\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m info",
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[34m   DEBUG\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m debug",
        ]

        configure_logger(logger, levels[level], stream, ansi=True)

        logger.critical("critical")
        logger.error("error")
        logger.warning("warning")
        logger.info("info")
        logger.debug("debug")

        out = stream.getvalue().strip().split("\n")
        assert len(out) == len(levels) - level

        for i, level in enumerate(levels[level:]):
            message = out[i]
            print(message)
            assert message == expected[i]

    @pytest.mark.parametrize("level", [0, 1, 2, 3, 4])
    def test_basename(self, logger, level):
        stream = io.StringIO()
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        expected = [
            "[2000-12-31 18:00:00.000] CRITICAL | test_logger: critical",
            "[2000-12-31 18:00:00.000]    ERROR | test_logger: error",
            "[2000-12-31 18:00:00.000]  WARNING | test_logger: warning",
            "[2000-12-31 18:00:00.000]     INFO | test_logger: info",
            "[2000-12-31 18:00:00.000]    DEBUG | test_logger: debug",
        ]

        configure_logger(logger, levels[level], stream, use_base_name=True)

        logger.critical("critical")
        logger.error("error")
        logger.warning("warning")
        logger.info("info")
        logger.debug("debug")

        out = stream.getvalue().strip().split("\n")

        assert len(out) == len(levels) - level

        for i, level in enumerate(levels[level:]):
            message = out[i]
            print(message)
            assert message == expected[i]

    def test_multiple_calls(self, logger):
        stream = io.StringIO()
        expected = [
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[31mCRITICAL\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m critical",
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[31m   ERROR\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m error",
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[33m WARNING\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m warning",
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[32m    INFO\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m info",
            "\x1b[38;5;8m2000-12-31 18:00:00.000\x1b[0m \x1b[34m   DEBUG\x1b[0m \x1b[38;5;8mtest_logger.logger\x1b[0m debug",
            "[2000-12-31 18:00:00.000] CRITICAL | test_logger.logger: critical",
            "[2000-12-31 18:00:00.000]    ERROR | test_logger.logger: error",
            "[2000-12-31 18:00:00.000]  WARNING | test_logger.logger: warning",
            "[2000-12-31 18:00:00.000] CRITICAL | test_logger.logger: critical",
            "[2000-12-31 18:00:00.000]    ERROR | test_logger.logger: error",
            "[2000-12-31 18:00:00.000]  WARNING | test_logger.logger: warning",
            "[2000-12-31 18:00:00.000]     INFO | test_logger.logger: info",
        ]

        configure_logger(logger, "DEBUG", stream, ansi=True)

        logger.critical("critical")
        logger.error("error")
        logger.warning("warning")
        logger.info("info")
        logger.debug("debug")

        configure_logger(logger, "WARNING", stream)

        logger.critical("critical")
        logger.error("error")
        logger.warning("warning")
        logger.info("info")
        logger.debug("debug")

        configure_logger(logger, "INFO", stream)

        logger.critical("critical")
        logger.error("error")
        logger.warning("warning")
        logger.info("info")
        logger.debug("debug")

        out = stream.getvalue().strip().split("\n")
        for a, b in zip(out, expected):
            print(a)
            assert a == b

        # assert len(out) == len(levels) - level

        # for i, level in enumerate(levels[level:]):
        #     message = out[i]
        #     print(message)
        #     assert message == expected[i]
